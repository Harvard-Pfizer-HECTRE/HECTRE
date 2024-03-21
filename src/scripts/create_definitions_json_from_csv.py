import csv
import json
import os

import click

'''
This generates the definitions.json in the root of the repo.
The CSV passed in is from the Harvard MBMA Data Definition file provided by Pfizer.
Likely we won't have to run it again, but who knows?
'''

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
def create_definitions(file_path: str):
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # Convert CSV data to list of dictionaries
        data = [row for row in reader]

    # Write data to JSON file
    output_path = os.path.join(os.path.dirname(__file__), "../../definitions.json")
    with open(output_path, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)

if __name__ == '__main__':
    create_definitions()