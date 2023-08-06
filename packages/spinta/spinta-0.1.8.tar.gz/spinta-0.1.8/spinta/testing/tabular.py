import csv
import pathlib
from typing import List

from spinta import commands
from spinta.core.config import RawConfig
from spinta.manifests.components import Manifest
from spinta.manifests.helpers import load_manifest_nodes
from spinta.manifests.tabular.constants import DATASET
from spinta.manifests.tabular.helpers import datasets_to_tabular
from spinta.manifests.tabular.helpers import read_ascii_tabular_rows
from spinta.manifests.tabular.helpers import read_tabular_manifest
from spinta.testing.context import create_test_context


def create_tabular_manifest(path: pathlib.Path, manifest: str):
    with path.open('w') as f:
        writer = csv.writer(f)
        rows = read_ascii_tabular_rows(manifest, strip=True)
        for row in rows:
            writer.writerow(row)


def load_tabular_manifest(rc: RawConfig, path: pathlib.Path) -> Manifest:
    rc = rc.fork({
        'manifest': 'default',
        'manifests': {
            'default': {
                'type': 'tabular',
                'path': str(path),
                'keymap': 'default',
            },
        },
    })

    context = create_test_context(rc)

    config = context.get('config')
    commands.load(context, config)

    store = context.get('store')
    commands.load(context, store)

    schemas = read_tabular_manifest(path)
    load_manifest_nodes(context, store.manifest, schemas)

    commands.link(context, store.manifest)

    return store.manifest


def render_tabular_manifest(manifest: Manifest, cols: List[str] = None) -> str:
    rows = datasets_to_tabular(manifest)
    cols = cols or DATASET
    hs = 1 if 'id' in cols else 0  # hierarchical cols start
    he = cols.index('property')    # hierarchical cols end
    hsize = 1                      # hierarchical column size
    bsize = 3                      # border size
    sizes = dict(
        [(c, len(c)) for c in cols[:hs]] +
        [(c, 1) for c in cols[hs:he]] +
        [(c, len(c)) for c in cols[he:]]
    )
    rows = list(rows)
    for row in rows:
        for i, col in enumerate(cols):
            val = '' if row[col] is None else str(row[col])
            if col == 'id':
                sizes[col] = 2
            elif i < he:
                size = (hsize + bsize) * (he - hs - i) + sizes['property']
                if size < len(val):
                    sizes['property'] += len(val) - size
            elif sizes[col] < len(val):
                sizes[col] = len(val)

    line = []
    for col in cols:
        size = sizes[col]
        line.append(col[:size].ljust(size))
    lines = [line]

    depth = 0
    for row in rows:
        if 'id' in cols:
            line = [row['id'][:2] if row['id'] else '  ']
        else:
            line = []

        for i, col in enumerate(cols[hs:he + 1]):
            val = row[col] or ''
            if val:
                depth = i
                break
        else:
            val = ''
            depth = 0

        line += [' ' * hsize] * depth
        size = (hsize + bsize) * (he - hs - depth) + sizes['property']
        line += [val.ljust(size)]

        for col in cols[he + 1:]:
            val = '' if row[col] is None else str(row[col])
            size = sizes[col]
            line.append(val.ljust(size))

        lines.append(line)

    lines = [' | '.join(line) for line in lines]
    lines = [l.rstrip() for l in lines]
    return '\n'.join(lines)
