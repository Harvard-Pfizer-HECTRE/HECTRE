from typing import Optional
import click
from hectre.api import extract_data
from hectre.cdf.cdf import CDF, CDFData
from pathlib import Path
import pandas as pd
from hectre.consts import HEADER_ORDER

@click.command()
@click.argument('path_to_pdf', type=str)
@click.argument('picos_string', type=str)
@click.argument('path_to_cdf', type=str)
def cdf_accuracy(path_to_pdf: str, picos_string: str, path_to_cdf: str):
    # path_to_pdf = Path(path_to_pdf)
    # path_to_cdf = Path(path_to_cdf)
    # cdf: Optional[CDF] = extract_data(file_path=path_to_pdf.resolve(), picos_string=picos_string)
    fake_cdf_r1 = CDFData(**{key:"zero" for key in HEADER_ORDER})
    cdf = CDF()
    cdf.add_clinical_data(fake_cdf_r1)
    cdf.set_literature_data(fake_cdf_r1)
    if not cdf:
        raise RuntimeError(f'HECTRE failed to produce a cdf for the PDF located at {path_to_pdf}')
    accuracy = cdf.compare()
    print(accuracy['test_lit_data'])
    print(accuracy['test_clin_data'])

if __name__ == '__main__':
    cdf_accuracy()
