
import logging
import sys

import click

from .api import extract_from_file_path
from .cdf.cdf import Cdf

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.argument('picos_string', type=str)
def extract_with_file_path(file_path: str, picos_string: str):
    # This will fail, since a lot of parts are not implemented yet
    cdf: Cdf = extract_from_file_path(file_path, picos_string)
    click.echo(str(cdf))


if __name__ == '__main__':
    extract_with_file_path()