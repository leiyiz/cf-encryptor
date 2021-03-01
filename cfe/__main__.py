import uuid
import errno, os, sys, cmd
import click, logging
import drive_api
import vault.crypto as crypto
import vault.storage as vault
from getpass import getpass
from paths import is_path_exists_or_creatable

@click.group()
def cli():
    pass

@click.command()
def init():
    # Create a folder where the CFE metadata will be stored
    if os.path.exists('vault/cfe_vault.dat'):
        os.utime('vault/cfe_vault.dat', None)
    else:
        os.mkdir('vault')
        open('vault/cfe_vault.dat', 'a').close()

@click.command()
@click.argument('add_type')
@click.argument('name')
def add (add_type, name):
    # Check if they are trying to add a provider
    # TODO: add login by name
    if add_type == "provider":
        drive_api.auth.drive_login()
        drive_api.func.init_folder(".cfe")

        print("Adding", name)
    else:
        logging.error(f"Error: Adding '{add_type}' is not supported.")


@click.command()
@click.argument('src')
@click.argument('dst')
def upload(src, dst):
    # TODO: Validate if the provider exists
    if not is_path_exists_or_creatable(src):
        logging.error(f"invalid path: {src}")
        return

    # Read the contents of the file
    content = None
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
    
    # Create a vault entrys
    password = getpass(prompt="Enter password for encryption:")
    v = vault.Vault(password)

    if v.get_data(f"{dst} ") is not None:
        logging.error(f"Already an entry for {dst}")
        return
    
    guid = str(uuid.uuid4())
    entry = v.create_data(f"{dst} {guid}")

    # Encrypt the data
    cipher = crypto.encrypt(entry.entry_key, content)

    # Upload it to the cloud
    drive_api.func.file_upload(guid + ".enc", cipher.decode(), ['.cfe'])
    logging.info(f"Successfully uploaded file as {guid}.enc")


@click.command()
@click.argument('src')
@click.argument('dst')
def download(src, dst):
    # Validate file paths
    if not is_path_exists_or_creatable(dst):
        logging.error(f"invalid path: {dst}")
        return

    # Make sure that we don't overwrite a file
    if os.path.isfile(dst):
        print(f"We have detected a file already at '{dst}'")
        if not click.confirm("Do you want to overwrite this file?", default=False):
            return

    # Get the file ID
    password = getpass(prompt="Enter password for encryption:")
    v = vault.Vault(password)
    entry = v.get_data(src + " ")

    if entry is None:
        logging.error(f"No metdata found on {src}")
        return

    key = entry.get_key()
    data = entry.get_name().split()
    nickname = data[0].strip()
    remote_name = data[1].strip()

    # Download the file
    cipher = None
    try:
        cipher = drive_api.func.file_download(remote_name + ".enc", ['.cfe'], dst)
    except:
        logging.error(f"Could not find {nickname}")
        return

    if cipher is None:
        logging.error(f"Could not find {nickname}")
        return

    # Decrypt the file and write to dst
    plaintext = crypto.decrypt(key, cipher)
    with open(dst, "wb") as f:
        f.write(plaintext)

    logging.info(f"Successfully downloaded {dst}")

@click.command()
def list():
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
@click.argument("filename")
def delete(filename):

    # Get the file ID
    password = getpass(prompt="Enter password for encryption:")
    v = vault.Vault(password)
    entry = v.get_data(filename + " ")

    if entry is None:
        logging.error(f"No metadata found on {filename}")
        return

    key = entry.get_key()
    data = entry.get_name().split()
    nickname = data[0].strip()
    remote_name = data[1].strip()
    # Delete the file
    try:
        drive_api.func.file_delete(remote_name + ".enc", ['.cfe'])
    except:
        logging.error(f"Could not find {nickname}")
        return

    success = v.delete_data(filename)
    if not success:
        logging.error(f"Could not find {nickname}")

    logging.info(f"Successfully deleted {filename}")
    

cli.add_command(init)
cli.add_command(add)
cli.add_command(download)
cli.add_command(upload)
cli.add_command(list)
cli.add_command(delete)

if __name__ == '__main__':
    cli()