import click, pprint

from ..cdf.cdf import *

'''
This file is used to run unit tests.
Define a new function, and give it the cli decorator to add it as a sub-command.
'''

@click.group()
def cli():
    pass

@cli.command()
def cdf():
    cdf: CDF = CDF.create()
    click.echo(cdf.model_dump_json())

@cli.command()
def lit_data():
    ld: CDFData = CDFData()
    click.echo(ld.model_dump())

@cli.command()
def test_alias():
    d = CDFData(**{"ARM.ROUTE": "route 66"})
    print(d)

@cli.command()
def test_cdf():
    lit = CDFData(**{"AU": "JFN:MM"})
    clin = CDFData(**{"ARM.ROUTE": "route 66"})
    cdf = CDF()
    cdf.literature_data = lit
    cdf.clinical_data = [clin]
    print(cdf)

@cli.command()
def test_add_to_cdf():
    lit = CDFData(**{"AU": "JFN:MM"})
    clin = CDFData(**{"ARM.ROUTE": "route 66"})
    cdf = CDF()
    cdf.literature_data = lit
    cdf.clinical_data = [clin]
    cdf.add_clinical_data({"ARM.ROUTE": "route 77"})
    print(cdf)

@cli.command()
def test_cdf_to_df():
    lit = CDFData(**{"AU": "JFN:MM"})
    clin = CDFData(**{"ARM.ROUTE": "route 66"})
    cdf = CDF()
    cdf.literature_data = lit
    cdf.clinical_data = [clin]
    cdf.add_clinical_data({"ARM.ROUTE": "route 77"})
    print(cdf.to_df())

@cli.command()
def test_cdf_to_csv():
    lit = CDFData(**{"AU": "JFN:MM"})
    clin = CDFData(**{"ARM.ROUTE": "route 66"})
    cdf = CDF()
    cdf.literature_data = lit
    cdf.clinical_data = [clin]
    cdf.add_clinical_data({"ARM.ROUTE": "route 77"})
    df = cdf.to_df()
    df.to_csv("test_output.csv")

@cli.command()
def test_from_json():
    lit = CDFData(**{"AU": "JFN:MM"})
    c1 = '{"BSL.LCI": 8.7}'
    c2 = '{"CHBSL.VARU": "SD"}'
    clin = CDFData.from_json(c1, c2)
    cdf = CDF()
    cdf.literature_data = lit
    cdf.clinical_data = [clin]
    print(cdf)

if __name__ == '__main__':
    cli()