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
    test_cdf: Optional[CDF] = extract_data(file_path=path_to_test_pdf.resolve(), picos_string=picos_string)
    if not test_cdf:
        raise RuntimeError(f'HECTRE failed to produce a cdf for the PDF located at {path_to_pdf}')
    # Create a DataFrame from the control CDF CSV.
    control_cdf = pd.read_csv(path_to_control_cdf.resolve())
    # Run the comparison.
    accuracy = test_cdf.compare(test_cdf.to_df(), control_cdf)
    print(f'MEASURING ACCURACY OF HECTRE EXTRACTION OF {path_to_pdf}:')
    print()
    print('CONTROL PRIMARY KEYS')
    print(accuracy['control_clin_data'].index)
    print()
    print('TEST PRIMARY KEYS')
    print(accuracy['test_clin_data'].index)
    print()
    print('ACCURACY OF LITERATURE DATA VALUES (indexed by column name):')
    print()
    lit_acc_pct = accuracy['comp_values_lit'].sum() / accuracy['comp_values_lit'].size
    print('Average string similarity (percent similar): ', f'{lit_acc_pct:.2f}')
    print()
    for col in accuracy['comp_values_lit'].index:
        print(f'{col}: ',  accuracy['comp_values_lit'][col])
    print()
    print('ACCURACY OF CLINICAL DATA ROWS (indexed by control compound primary key):')
    print()
    for i, row in accuracy['comp_rows_clin'].iterrows():
        print(i)
        print(row.to_string())
        print()
    print()
    print('ACCURACY OF CLINICAL DATA COLUMNS (indexed by column name):')
    print()
    for col in accuracy['comp_values_clin'].columns:
        pct = (accuracy['comp_values_clin'][col].sum() / accuracy['comp_values_clin'].shape[0]) * 100
        print(f'{col}: ', f'{pct:.2f}')
    print()
    print('ROW 1 OF THE MATCHED CDFs: TEST vs. CONTROL')
    print()
    test_control_clin_join = accuracy['control_clin_data'].merge(accuracy['test_clin_data'], left_index=True, right_index=True)
    # If test and control have at least one matching row, display an example.
    if test_control_clin_join.shape[0] > 0:
        # Index of first row in the joined df. Should exist in test and control.
        matched_compound_key = test_control_clin_join.index[0]
        test_r1 = pd.concat([accuracy['test_lit_data'], accuracy['test_clin_data'].loc[matched_compound_key]])
        control_r1 = pd.concat([accuracy['control_lit_data'], accuracy['control_clin_data'].loc[matched_compound_key]])
        df_r1 = pd.DataFrame(data={'Test': test_r1.to_list(), 'Control': control_r1.to_list()}, index=test_r1.index, columns=['Test', 'Control'])
        pd.set_option('display.max_rows', df_r1.shape[0])
        print(df_r1)
    else:
        print()
    print('None of the test and control compound primary keys matched')

if __name__ == '__main__':
    cdf_accuracy()
