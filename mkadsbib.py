#!/usr/bin/env python3

import click
import os
import re
from contextlib import closing

__version__ = '0.1'

@click.group()
@click.option("--sandbox/--no-sandbox", default=False, help="Query against the ads sandbox.")
@click.option("--ads-api-key", envvar="ADS_DEV_KEY", help="ADS API Key")
def main(sandbox, ads_api_key):
    """Make bibliographies"""
    global ads
    if sandbox:
        import ads.sandbox as ads
    else:
        import ads
    ads.config.token = ads_api_key
    
@main.command()
@click.argument('input', type=click.File(mode='r'))
@click.option("-o", "--output", default=None, help="Output file name.")
def transform(input):
    """Transform a list of bibcodes to bib entries."""
    bibcodes = [line for line in input]
    with open_output(output, input.name, extension='.bib') as f:
        f.write(ads.ExportQuery(bibcodes).execute())

def parse(lines, root="."):
    """Parse a line."""
    for line in lines:
        citation = re.match(r'\\citation\{([\S]+)\}', line)
        if citation:
            yield from citation.group(1).split(",")
        fileinput = re.match(r'\\@?input\{([\S]+)\}', line)
        if fileinput:
            with open(os.path.join(root, fileinput.group(1)), 'r') as subfile:
                yield from parse(subfile, os.path.dirname(subfile.name))

def get_aux_file(file_obj):
    """Return an .aux file object."""
    if os.path.splitext(file_obj.name)[1] == ".tex":
        file_obj.close()
        file_obj = open("{0}.aux".format(os.path.splitext(file_obj.name)[0]), 'r')
    return file_obj

def open_output(output_name, input_name, extension, mode='w'):
    """Return a file suitable for output"""
    if output_name is None:
        output_name = "{0}{1}".format(os.path.splitext(input_name)[0], extension)
    return open(output_name, mode)

@main.command()
@click.option("-o", "--output", default=None, help="Output file name.")
@click.argument('input', type=click.File(mode='r'))
def extract(input, output):
    """Extract citations"""
    with closing(get_aux_file(input)) as aux_file:
        with open_output(output, input.name, extension='.bbq') as f:
            for citation in parse(input):
                f.write(citation)
                f.write("\n")
    

@main.command()
@click.option("-o", "--output", default=None, help="Output file name.")
@click.argument('input', type=click.File(mode='r'))
def make(input, output):
    """Make bibliography in one go."""
    with closing(get_aux_file(input)) as aux_file:
        bibcodes = list(parse(aux_file, os.path.dirname(aux_file.name)))
        click.echo("Extracted bibcodes from {0}".format(aux_file.name))
    with open_output(output, input.name, extension=".bib") as f:
        f.write(ads.ExportQuery(bibcodes).execute())
        click.echo("Wrote bibliography to {0}".format(f.name))

if __name__ == '__main__':
    main()