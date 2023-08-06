__version__ = "0.1.0"

import ast
import click
import json
import re
import sys

@click.command()
@click.option('--literal', required=False)
@click.argument('input_file', required=False, type=click.File('r'))
@click.option('--lines', required=False, is_flag=True)
@click.option('--pretty', required=False, is_flag=True)
def main(literal, input_file, lines, pretty):
    '''
    Convert from Python dict literal to JSON
    '''
    converted = convert(literal, input_file, lines, pretty)
    if lines:
        for converted_line in converted:
            click.echo(converted_line)
    else:
        click.echo(converted)

def convert(literal=None, input_file=None, lines=False, pretty=False):
    if literal:
        contents = literal
    else:
        if not input_file:
            input_file = sys.stdin
        contents = input_file.read().strip()

    if not contents:
        return

    if lines:
        return _convertLines(contents, pretty)
    else:
        return _convert(contents, pretty)

def _convertLines(contents, pretty):
    for line in re.split("[\r\n]{1,2}", contents):
        yield _convert(line, pretty)

def _convert(text, pretty=False):
    d = ast.literal_eval(text)
    if pretty:
        return json.dumps(d, indent=2)
    else:
        return json.dumps(d)

