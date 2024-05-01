import pandas as pd
from pathlib import Path
import os

import click

'''
Takes a CDF csv containing multiple articles and creates an individual CDF csv for each article.

Creates files in the containing directory.
'''

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path(exists=True))
def create_cdfs(file_path: str, output_path: str):
    file_path = Path(file_path)
    pdf_slugs = Path('hectre/tests/test_data').glob('*.pdfdata')
    pdf_slugs = {file.stem.split('_')[0]:file.stem for file in pdf_slugs}
    if file_path.suffix == '.xlsx':
        multi_df = pd.read_excel(file_path.resolve())
    elif file_path.suffix == '.csv':
        multi_df = pd.read_csv(file_path.resolve())
    else:
        raise ValueError(f'This script only accepts .csv or .xlsx, you passed a {file_path.suffix}')
    for dsid in multi_df['DSID'].unique():
        df = multi_df[multi_df['DSID'] == dsid]
        if pdf_slugs.get(str(dsid)):
            df.to_csv(path_or_buf=f'{output_path}/{pdf_slugs[str(dsid)]}.csv', index=False)

if __name__ == '__main__':
    create_cdfs()