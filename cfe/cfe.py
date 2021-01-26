import click

@click.group()
def cli():
    pass

@click.command()
def add_provider():
    click.echo('add_provider')

@click.command()
def download():
    click.echo('download')

@click.command()
def init():
    click.echo('init')

@click.command()
def upload():
    click.echo('upload')

cli.add_command(add_provider)
cli.add_command(download)
cli.add_command(init)
cli.add_command(upload)

if __name__ == '__main__':
    cli()