import click

@click.group()
def cli():
    pass

@click.command()
@click.argument('name')
def add_provider(name):
    # Prompt Google Drive login information

    # Save the provider name and relevant information

    click.echo('add_provider')

@click.command()
@click.argument('src')
@click.argument('dst')
def download(src, dst):
    # Get the file ID

    # Download the file

    # Decrypt the file

    # Check for the canary

    click.echo('download')

@click.command()
def init():
    # Create a folder where the CFE metadata will be stored
    click.echo('init')

@click.command()
@click.argument('src')
@click.argument('dst')
def upload(src, dst):
    # Encrypt the file

    # Validate if the provider exists

    # Upload it to the cloud

    # Get the file ID and save it

    click.echo('upload')

cli.add_command(add_provider)
cli.add_command(download)
cli.add_command(init)
cli.add_command(upload)

if __name__ == '__main__':
    cli()