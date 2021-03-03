import cmd
import logging
import os
import uuid
from getpass import getpass
from shutil import rmtree

import click
import tqdm

import drive_api.auth as auth
import drive_api.func as func
import vault.crypto as crypto
import vault.storage as vault
from paths import is_path_exists_or_creatable

GIGABYTE_SIZE: int = 1073741824
ROOT_DIR: str = '.cfe'


@click.group()
def cli():
    """
    Instantiates the CLI application.
    """
    pass


@click.command()
def login():
    """
    Login to gDrive and Initializes a CFE vault.
    """
    # Create a folder where the CFE metadata will be stored
    dat_path: str = vault.__get_dat_path()
    if os.path.exists(dat_path):
        os.utime(dat_path, None)
    else:
        os.mkdir(vault.VAULT_DIR)
        open(dat_path, 'a').close()
    __download_vault_if_exist()


@click.command()
@click.argument('add_type')
@click.argument('name')
def add(add_type, name):
    """
    Given a type of entity and a label of the entity, adds the entity with the label to the CFE application.
    """
    # Check if they are trying to add a provider
    # TODO: add login by name
    # TODO: deprecate this method
    if add_type == "provider":
        auth.drive_login()
        func.init_folder(ROOT_DIR)

        print("Adding", name)
    else:
        logging.error(f"Error: Adding '{add_type}' is not supported.")


@click.command()
def logout():
    auth.drive_logout()
    if os.path.exists('vault'):
        rmtree('vault')
    print("You have logged out from cfe")


def __download_vault_if_exist():
    try:
        dat_path = vault.__get_dat_path()
        content: bytes = func.file_download(dat_path, [ROOT_DIR, 'meta'])
        with open(dat_path, 'wb') as file:
            file.write(content)
    except FileNotFoundError:
        return


@click.command()
@click.argument('src')
@click.argument('dst')
def upload(src, dst):
    """
    Uploads a local file at src at the given alias destination.
    """
    # TODO: Validate if the provider exists
    if not is_path_exists_or_creatable(src):
        logging.error(f"invalid path: {src}")
        return

    __download_vault_if_exist()

    # Read the contents of the file
    try:
        with open(src, 'rb') as f:
            content = f.read()
    except Exception as e:
        print(e)
        logging.error(f"Error: Could not find file {src}")
        return

    if content is None:
        logging.error(f"Error: Could not find file {src}")
        return

    # If it's a file, make sure that the file is not too large
    if os.stat(src).st_size >= GIGABYTE_SIZE:
        logging.error(f"file exceeds 1GiB: {src}")
        return

    # Get the password and have the user reconfirm it
    password = getpass(prompt="Enter password for encryption:")
    retyped_password = getpass(prompt="Confirm your password:")

    # If the password and the retyped password don't match, have the user retype the pairs
    # until they match
    while password != retyped_password:
        logging.warning('Passwords do not match. Please try again.\n')

        password = getpass(prompt="Enter password for encryption:")
        retyped_password = getpass(prompt="Confirm your password:")

    # Create a vault entries
    v = vault.Vault(password)

    if v.get_data(f"{dst} ") is not None:
        logging.error(f"Already an entry for {dst}")
        return

    with tqdm.tqdm(total=100) as progress_bar:
        guid = str(uuid.uuid4())
        entry = v.create_data(f"{dst} {guid}")

        progress_bar.update(33)  # Increment progress bar by 33%

        # Encrypt the data
        cipher = crypto.encrypt(entry.entry_key, content)

        progress_bar.update(34)  # Increment progress bar by 34%

        # Upload it to the cloud
        func.file_upload(guid + ".enc", cipher.decode(), [ROOT_DIR])
        func.file_replace(vault.__get_dat_path(), None, [ROOT_DIR, 'meta'])
        logging.info(f"Successfully uploaded file as {guid}.enc")

        progress_bar.update(33)  # Increment progress bar by 33%


@click.command()
@click.argument('src')
@click.argument('dst')
def download(src, dst):
    """
    Downloads the file at src with and saves it at the local location at dst.
    """
    # Validate file paths
    if not is_path_exists_or_creatable(dst):
        logging.error(f"invalid path: {dst}")
        return

    __download_vault_if_exist()

    # Make sure that we don't overwrite a file
    if os.path.isfile(dst):
        print(f"We have detected a file already at '{dst}'")
        if not click.confirm("Do you want to overwrite this file?", default=False):
            return

    # Get the file ID
    password = getpass(prompt="Enter password for encryption:")
    v = vault.Vault(password)
    entry = v.get_data(src + " ")

    with tqdm.tqdm(total=100) as progress_bar:
        if entry is None:
            logging.error(f"No metdata found on {src}")
            return

        progress_bar.update(33)  # Increment progress bar by 33%

        key = entry.get_key()
        data = entry.get_name().split()
        nickname = data[0].strip()
        remote_name = data[1].strip()

        # Download the file
        cipher = None
        try:
            cipher = func.file_download(remote_name + ".enc", [ROOT_DIR])
        except:
            logging.error(f"Could not find {nickname}")
            return

        if cipher is None:
            logging.error(f"Could not find {nickname}")
            return

        progress_bar.update(34)  # Increment progress bar by 34%

        # Decrypt the file and write to dst
        plaintext = crypto.decrypt(key, cipher)
        with open(dst, "wb") as f:
            f.write(plaintext)

        logging.info(f"Successfully downloaded {dst}")

        progress_bar.update(33)  # Increment progress bar by 33%


@click.command()
def list():
    """
    Lists all the files associated with a particular password.
    """
    # Prompt the user for a password
    password = getpass(prompt="Enter password for encryption:")
    v = vault.Vault(password)

    tmp = []
    for entry in v.get_data_list():
        data = entry.get_name().split()
        tmp.append(data[0].strip())

    tmp = sorted(tmp)
    cmd.Cmd().columnize(tmp, displaywidth=80)


@click.command()
@click.argument('filename')
def delete(filename):
    """
    Deletes a file in the vault with the given password.
    """
    __download_vault_if_exist()
    # Get the file ID
    password = getpass(prompt="Enter password for encryption:")
    v = vault.Vault(password)
    entry = v.get_data(filename + " ")

    if entry is None:
        logging.error(f"No metadata found on {filename}")
        return

    with tqdm.tqdm(total=100) as progress_bar:
        key = entry.get_key()
        data = entry.get_name().split()
        nickname = data[0].strip()
        remote_name = data[1].strip()
        # Delete the file
        try:
            func.file_delete(remote_name + '.enc', [ROOT_DIR])
        except:
            logging.error(f"Could not find {nickname} on cloud")
            return

        progress_bar.update(50)  # Increment progress bar by 50%

        success = v.delete_data(filename)
        if not success:
            logging.error(f"Could not find {nickname}")
        func.file_replace(vault.__get_dat_path(), None, [ROOT_DIR, 'meta'])

        progress_bar.update(50)  # Increment progress bar by 50%
        logging.info(f"Successfully deleted {filename}")


cli.add_command(add)  # TODO: deprecate this command
cli.add_command(login)
cli.add_command(logout)
cli.add_command(download)
cli.add_command(upload)
cli.add_command(list)
cli.add_command(delete)

if __name__ == '__main__':
    cli()
