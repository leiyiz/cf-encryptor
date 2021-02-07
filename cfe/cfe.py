import os
import uuid
import click
import logging
import drive_api
import vault.crypto as crypto
import vault.storage as vault
from getpass import getpass

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
def add(add_type, name):
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
    
    # Read the contents of the file
    content = None
    try:
        with open(src) as f:
            content = f.read()
    except:
        logger.error(f"Error: Could not find file {src}")
        return

    if content is None:
        logger.error(f"Error: Could not find file {src}")
        return
    
    # Create a vault entrys
    password = getpass(prompt="Enter password for encryption:")
    v = vault.Vault(password)

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
    with open(dst, "w") as f:
        f.write(plaintext.decode())

    logging.info(f"Successfully downloaded {dst}")


cli.add_command(init)
cli.add_command(add)
cli.add_command(download)
cli.add_command(upload)

if __name__ == '__main__':
    cli()