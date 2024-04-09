from datetime import datetime
import glob
import os

import click
from typing import Optional

from .api import extract_data
from .cdf.cdf import CDF
import logging


logger = logging.getLogger(__name__)


'''
This file is used to run a full execution on a PDF file, either locally or with an URL.
'''


@click.command()
@click.argument('path', type=str)
@click.argument('picos_string', type=str)
def extract(path: str, picos_string: str):
    file_paths = []
    urls = []
    if path.startswith("http"):
        # Not implementing batch URL processing here from an URL "folder",
        # rather, just call this in a loop in the web back-end.
        urls.append(path)
    else:
        if not os.path.exists(path):
            logger.error(f"Path does not exist: {path}")
            return
        if not os.path.isdir(path):
            file_paths.append(path)
        else:
            file_paths.extend(glob.glob(os.path.join(path, "*.pdf")))

    if file_paths:
        logger.info(f"Found {len(file_paths)} file(s)")
    if urls:
        logger.info(f"Found {len(urls)} URL(s)")

    for file_path in file_paths:
        cdf: Optional[CDF] = extract_data(file_path=file_path, picos_string=picos_string)
        if cdf:
            output_filename = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            cdf.save_to_file(output_filename)
        else:
            logger.error(f"Could not get resulting CDF! Is the path correct: {file_path}")

    for url in urls:
        cdf: Optional[CDF] = extract_data(url=url, picos_string=picos_string)
        if cdf:
            output_filename = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            cdf.save_to_file(output_filename)
        else:
            logger.error(f"Could not get resulting CDF! Is the URL correct: {url}")


if __name__ == '__main__':
    extract()