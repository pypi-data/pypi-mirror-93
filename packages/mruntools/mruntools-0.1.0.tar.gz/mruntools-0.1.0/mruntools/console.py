import pathlib

import click

from runtools.spec import get_all_specs


@click.command()
@click.argument("working_dir")
def list_working_dir(working_dir):

    specs = get_all_specs(working_dir)
    reprs = [spec.__repr__() for spec in specs]
    print('\n'.join(sorted(reprs)))
