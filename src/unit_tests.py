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

if __name__ == '__main__':
    cli()