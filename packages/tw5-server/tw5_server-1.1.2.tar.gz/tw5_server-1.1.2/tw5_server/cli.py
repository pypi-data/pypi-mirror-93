import click
from .app import app
from .config import CONFIG
from .storage import GitStorage


@app.cli.command('create-wiki')
@click.argument('name')
def create_wiki(name):
    storage = GitStorage.create(name)
    msg = f'wiki "{name}" is created. Dir is {storage.dirpath}'
    click.echo(msg)
