import click

from spinta import commands
from spinta.components import Context
from spinta.components import Store


def load_store(context: Context) -> Store:
    config = context.get('config')
    commands.load(context, config)
    commands.check(context, config)
    store = context.get('store')
    commands.load(context, store)
    return store


def prepare_store(context: Context) -> Store:
    store = load_store(context)
    commands.link(context, store)
    commands.check(context, store)
    commands.prepare(context, store)
    return store


def prepare_manifest(context: Context) -> Store:
    store = load_store(context)
    click.echo(f"Loading manifest {store.manifest.name}...")
    commands.load(context, store.manifest)
    commands.link(context, store.manifest)
    commands.check(context, store.manifest)
    commands.prepare(context, store.manifest)
    return store
