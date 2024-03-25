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
    # This will fail, since a lot of parts are not implemented yet
    cdf: CDF = CDF.create()
    click.echo(cdf.model_dump_json())


if __name__ == '__main__':
    cli()