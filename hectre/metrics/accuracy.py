import logging
from typing import Optional
from pathlib import Path
import click
import pandas as pd
from hectre.api import extract_data
from hectre.cdf.cdf import CDF

logger = logging.getLogger(__name__)

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
    logger.info(f'\nACCURACY OF HECTRE EXTRACTION: {path_to_pdf}:')
    logger.info(f"\nMatched control rows: {accuracy['num_matched_rows']} of {accuracy['control_clin_data'].shape[0]}")
    logger.info(f"\nCONTROL PRIMARY KEYS\n{accuracy['control_clin_data'].index}")
    logger.info(f"\nTEST PRIMARY KEYS\n{accuracy['test_clin_data'].index}")
    lit_acc_pct = accuracy['comp_values_lit'].sum() / accuracy['comp_values_lit'].size
    lit_vals = []
    for col in accuracy['comp_values_lit'].index:
        lit_vals.append(f"{col}: {accuracy['comp_values_lit'][col]}")
    avg_lit_acc = f'\nAverage string similarity (percent similar): {lit_acc_pct:.2f}\n'
    lit_vals_str = '\n'.join(lit_vals)
    logger.info(f"\nACCURACY OF LITERATURE DATA VALUES (indexed by column name):\n{avg_lit_acc}\n{lit_vals_str}")
    clin_data_rows = []
    for i, row in accuracy['comp_rows_clin'].iterrows():
        clin_data_rows.append(f'\n{i}\n{row.to_string()}')
    clin_data_rows_str = '\n'.join(clin_data_rows)
    logger.info(f"\nACCURACY OF CLINICAL DATA ROWS (indexed by control compound primary key):\n{clin_data_rows_str}")
    clin_data_cols = []
    for col in accuracy['comp_values_clin'].columns:
        pct = (accuracy['comp_values_clin'][col].sum() / accuracy['comp_values_clin'].shape[0]) * 100
        clin_data_cols.append(f'{col}: {pct:.2f}')
    clin_data_cols_str = '\n'.join(clin_data_cols)
    logger.info(f"\nACCURACY OF CLINICAL DATA COLUMNS (indexed by column name):\n{clin_data_cols_str}")
    # Check if there are any matching rows.
    test_control_clin_join = accuracy['control_clin_data'].merge(accuracy['test_clin_data'], left_index=True, right_index=True)
    # If test and control have at least one matching row, display an example.
    if test_control_clin_join.shape[0] > 0:
        logger.info('\nROW 1 OF THE MATCHED CDFs: TEST vs. CONTROL')
        # Index of first row in the joined df. Should exist in test and control.
        matched_compound_key = test_control_clin_join.index[0]
        test_r1 = pd.concat([accuracy['test_lit_data'], accuracy['test_clin_data'].loc[matched_compound_key]])
        control_r1 = pd.concat([accuracy['control_lit_data'], accuracy['control_clin_data'].loc[matched_compound_key]])
        df_r1 = pd.DataFrame(data={'Test': test_r1.to_list(), 'Control': control_r1.to_list()}, index=test_r1.index, columns=['Test', 'Control'])
        pd.set_option('display.max_rows', df_r1.shape[0])
        logger.info(df_r1)
    else:
        logger.info('\nNone of the test and control compound primary keys matched\n')

if __name__ == '__main__':
    cdf_accuracy()
