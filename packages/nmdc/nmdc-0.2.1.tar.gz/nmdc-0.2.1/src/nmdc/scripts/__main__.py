"""
CLI tools for NMDC
"""
import click
import json

import jsonschema
from jsonschema import validate

from nmdc import __version__
from nmdc.scripts.gff2json import NMDCGFFLoader


@click.group(help=f"""NMDC Tools v{__version__}.""")
def nmdccli():
    """
    NMDC command line tools.
    """
    pass


@nmdccli.command()
@click.argument('gff', type=click.File('r'))
@click.option('-of',
              help='output file name for genome feature json',
              required=True,
              type=click.File(mode='w'))
@click.option('-oa',
              help='output file name for functioanl annotation json',
              required=True,
              type=click.File(mode='w'))
@click.option('-ai',
              help='Activity index',
              required=True,
              type=str)
def gff2json(gff, of, oa, ai):
    """
    Convert GFF3 to NMDC JSON format.
    """
    INDENT = 2
    converter = NMDCGFFLoader(gff, ai)
    jobj = converter.model
    features = []
    annotations = []
    for record in jobj.keys():
        for feature in jobj[record].keys():
            entry = jobj[record][feature]
            features.append(entry['genome_feature_set'])
            annotations.extend(list(entry['functional_annotation_set'].values()))
    of.write(json.dumps({'genome_feature_set': features}, indent=INDENT))
    oa.write(json.dumps({'functional_annotation_set': annotations}, indent=INDENT))


@nmdccli.command('validate')
@click.option('--schema', help='The NMDC metadata JSON Schema', required=True, type=click.Path())
@click.option('--file', help='The file with JSON data to validate', required=True, type=click.Path())
def validate_json(schema, file):
    """
    Validate JSON as per NMDC Metadata schema.
    """
    try:
        validate(instance=json.load(open(file)), schema=json.load(open(schema)))
        print("Given JSON data is valid")
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        print("Given JSON data is not valid")


if __name__ == '__main__':
    nmdccli()
