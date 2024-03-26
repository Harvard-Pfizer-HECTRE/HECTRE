import click

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
    cdf_df = cdf.to_df()
    #click.echo(cdf_df)
    cdf_df.to_csv("test_output.csv")


if __name__ == '__main__':
    extract_with_file_path()