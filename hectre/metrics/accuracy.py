import logging
from typing import Optional
from pathlib import Path
import click
import pandas as pd
import numpy as np
from hectre.api import extract_data
from hectre.cdf.cdf import CDF

logger = logging.getLogger(__name__)

@click.command()
@click.argument('path_to_pdf', type=str)
@click.argument('picos_string', type=str)
@click.argument('path_to_cdf', type=str)
def cdf_accuracy_cmd(path_to_pdf: str, picos_string: str, path_to_cdf: str):
    test_cdf = accuracy_extract_test(path_to_pdf=path_to_pdf, picos_string=picos_string, path_to_cdf=path_to_cdf)
    # Create a DataFrame from the control CDF CSV.
    control_cdf = pd.read_csv(path_to_cdf)
    slug = Path(path_to_cdf).stem.lower()
    cdf_accuracy(test_cdf, control_cdf, slug)

def accuracy_extract_test(path_to_pdf: str, picos_string: str):
    test_cdf = extract_data(file_path=path_to_pdf, picos_string=picos_string)
    if not test_cdf:
        raise RuntimeError(f'HECTRE failed to produce a cdf for the PDF located at {path_to_pdf}')
    return test_cdf.to_df()

def cdf_accuracy(test_cdf: pd.DataFrame, control_cdf: pd.DataFrame, article_slug: str):
    """
    Measure the accuracy of a test CDF compared to a control CDF (considered 100% accurate).
    """
    # Run the comparison.
    accuracy = CDF.compare(test_cdf, control_cdf)
    logger.info(f'\nACCURACY OF HECTRE EXTRACTION: {article_slug}:')
    lit_acc_pct = accuracy['comp_values_lit'].sum() / accuracy['comp_values_lit'].size
    lit_vals = []
    for col in accuracy['comp_values_lit'].index:
        lit_vals.append(f"{col}: {accuracy['comp_values_lit'][col]}")
    avg_lit_acc = f'\nAverage string similarity (percent similar): {lit_acc_pct:.2f}\n'
    lit_vals_str = '\n'.join(lit_vals)
    logger.info(f"\nACCURACY OF LITERATURE DATA VALUES (indexed by column name):\n{avg_lit_acc}\n{lit_vals_str}")
    num_control_rows = accuracy['control_clin_data'].shape[0]
    matched_control_rows = num_control_rows - accuracy['row_matches_clin']['Matched Test Row'].isna().sum() 
    logger.info(f"\nMatched control rows: {matched_control_rows} of {num_control_rows}")
    logger.info(f"\nCONTROL ROW MATCHES\n{accuracy['row_matches_clin']}")
    clin_data_col_accs = accuracy['comp_values_clin'].mean()
    clin_data_cols = []
    for col, val in clin_data_col_accs.items():
        clin_data_cols.append(f'{col}: {val:.2f}')
    clin_data_cols_str = '\n'.join(clin_data_cols)
    logger.info(f"\nACCURACY OF CLINICAL DATA COLUMNS (indexed by column name):\n{clin_data_cols_str}")
    # If test and control have at least one matching row, display an example.
    if matched_control_rows > 0:
        logger.info('\nROW 1 OF THE MATCHED CDFs: TEST vs. CONTROL')
        # Index of first row in the joined df. Should exist in test and control.
        matched_rows = accuracy['row_matches_clin'][accuracy['row_matches_clin']['Matched Test Row'] != np.NaN]
        matched_control_key = matched_rows.index[0]
        matched_test_key = matched_rows.loc[matched_control_key, 'Matched Test Row']
        test_r1 = pd.concat([accuracy['test_lit_data'], accuracy['test_clin_data'].loc[matched_test_key]])
        control_r1 = pd.concat([accuracy['control_lit_data'], accuracy['control_clin_data'].loc[matched_control_key]])
        df_r1 = pd.DataFrame(data={'Test': test_r1.to_list(), 'Control': control_r1.to_list()}, index=test_r1.index, columns=['Test', 'Control'])
        pd.set_option('display.max_rows', df_r1.shape[0])
        logger.info(df_r1)
    else:
        logger.info('\nNone of the test and control compound primary keys matched\n')
    return {
        'comparison': accuracy,
        'lit_acc_pct': lit_acc_pct,
        'num_control_rows': num_control_rows,
        'matched_control_rows': matched_control_rows,
        'clin_data_col_accs': clin_data_col_accs
    }

if __name__ == '__main__':
    cdf_accuracy_cmd()
