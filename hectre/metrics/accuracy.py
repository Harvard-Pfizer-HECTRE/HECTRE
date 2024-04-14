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
    path_to_test_pdf = Path(path_to_pdf)
    path_to_control_cdf = Path(path_to_cdf)
    path_to_fake_control_cdf = Path("hectre/tests/test_data/cdfs/fake_305_deBruin_2018.csv")
    # test_cdf: Optional[CDF] = extract_data(file_path=path_to_test_pdf.resolve(), picos_string=picos_string)
    ### FAKE TEST CDF
    fake_test_cdf_r1 = CDFData(**{key:"zero" for key in HEADER_ORDER if key != 'DSID'})
    test_cdf = CDF()
    test_cdf.add_clinical_data(fake_test_cdf_r1)
    test_cdf.set_literature_data(fake_test_cdf_r1)
    if not test_cdf:
        raise RuntimeError(f'HECTRE failed to produce a cdf for the PDF located at {path_to_pdf}')
    # Create a DataFrame from the control CDF CSV.
    control_cdf = pd.read_csv(path_to_control_cdf.resolve())
    # Create a FAKE DataFrame from the control CDF CSV.
    fake_control_cdf = pd.read_csv(path_to_fake_control_cdf.resolve());
    accuracy = test_cdf.compare(control_cdf, fake_control_cdf)
    print('ACCURACY OF CLINICAL DATA ROWS (indexed by control compound primary key):')
    for i, row in accuracy['comp_rows'].iterrows():
        print(i)
        print(row.to_string())
    print('ACCURACY OF CLINICAL DATA COLUMNS (indexed by column name):')
    for col in accuracy['comp_values'].columns:
        pct = (accuracy['comp_values'][col].sum() / accuracy['comp_values'].shape[0]) * 100
        print(f'{col}: ', f'{pct:.2f}')

if __name__ == '__main__':
    cdf_accuracy()
