import click, pprint

from cdf.cdf import *

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
    ld: LiteratureData = LiteratureData()
    click.echo(ld.model_dump())

@cli.command()
def getfielddefs():
    get_field_defs()
    #click.echo(ld.model_dump())

@cli.command()
def test_alias():
    d = ClinicalData(**{"ARM.ROUTE": "route 66"})
    print(d)

@cli.command()
def test_cdf():
    lit = LiteratureData(**{"AU": "JFN:MM"})
    clin = ClinicalData(**{"ARM.ROUTE": "route 66"})
    cdf = CDF()
    cdf.literature_data = lit
    cdf.clinical_data = [clin]
    print(cdf)

@cli.command()
def test_add_to_cdf():
    lit = LiteratureData(**{"AU": "JFN:MM"})
    clin = ClinicalData(**{"ARM.ROUTE": "route 66"})
    cdf = CDF()
    cdf.literature_data = lit
    cdf.clinical_data = [clin]
    cdf.add_clinical_data({"ARM.ROUTE": "route 77"})
    print(cdf)

@cli.command()
def test_cdf_to_df():
    lit = LiteratureData(**{"AU": "JFN:MM"})
    clin = ClinicalData(**{"ARM.ROUTE": "route 66"})
    cdf = CDF()
    cdf.literature_data = lit
    cdf.clinical_data = [clin]
    cdf.add_clinical_data({"ARM.ROUTE": "route 77"})
    print(cdf.to_df())

@cli.command()
def test_cdf_to_csv():
    lit = LiteratureData(**{"AU": "JFN:MM"})
    clin = ClinicalData(**{"ARM.ROUTE": "route 66"})
    cdf = CDF()
    cdf.literature_data = lit
    cdf.clinical_data = [clin]
    cdf.add_clinical_data({"ARM.ROUTE": "route 77"})
    df = cdf.to_df()
    df.to_csv("test_output.csv")

if __name__ == '__main__':
    cli()