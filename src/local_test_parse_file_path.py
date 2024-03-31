import click
from datetime import datetime

from .api import extract_data
from .cdf.cdf import CDF
import logging
logger = logging.getLogger(__name__)


'''
This file is used to run a full execution on a PDF file locally.
'''


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.argument('picos_string', type=str)
def extract_with_file_path(file_path: str, picos_string: str):
    # This will fail, since a lot of parts are not implemented yet
    cdf: CDF = extract_data(file_path=file_path, picos_string=picos_string)
    output_filename = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    cdf.save_to_file(output_filename)


if __name__ == '__main__':
    extract_with_file_path()