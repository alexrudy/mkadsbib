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
def query(input, output):
    """Transform a list of bibcodes to bib entries."""
    bibcodes = [line for line in input]
    with open_output(output, input.name, extension='.bib') as f:
        f.write(ads.ExportQuery(bibcodes).execute())
    click.echo("Exported BibTeX to {0}.".format(f.name))


def parse(lines, root="."):
    """Parse a line."""
    for line in lines:
        # ADS Bibcodes always start with the year.
        citation = re.match(r'\\citation\{([^\s]+)\}', line)
        if citation:
            for citekey in citation.group(1).split(","):
                if re.match(r"[0-9]{4}[^\s]+", citekey):
                    yield citekey
        fileinput = re.match(r'\\@?input\{([\S]+)\}', line)
        if fileinput:
            subfile_name = find_aux_file(os.path.join(root, fileinput.group(1)))
            with open(subfile_name, 'r') as subfile:
                yield from parse(subfile, os.path.dirname(subfile.name))

def find_aux_file(filename):
    """Find aux file, check for latex-out folder."""
    auxfile = "{0}.aux".format(os.path.splitext(filename)[0])
    if os.path.exists(auxfile):
        return auxfile
    auxout = os.path.join('latex.out', os.path.relpath(auxfile))
    if os.path.exists(auxout):
        return auxout
    raise FileNotFoundError("Can't locate .aux file for {0}".format(filename))


def get_aux_file(file_obj):
    """Return an .aux file object."""
    if os.path.splitext(file_obj.name)[1] == ".tex":
        file_obj.close()
        file_obj = open(find_aux_file(file_obj.name), 'r')
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
            for citation in sorted(set(parse(aux_file))):
                f.write(citation)
                f.write("\n")
    click.echo("Extracted bibcodes from {0} into {1}.".format(input.name, f.name))

@main.command()
@click.option("-o", "--output", default=None, help="Output file name.")
@click.option("--bbq/--no-bbq", default=False, help="Output bibcode listing.")
@click.argument('input', type=click.File(mode='r'))
def make(input, output, bbq):
    """Make bibliography in one go."""
    with closing(get_aux_file(input)) as aux_file:
        bibcodes = sorted(set(parse(aux_file, os.path.dirname(aux_file.name))))
        click.echo("Extracted {0} bibcodes from {1}".format(len(bibcodes), aux_file.name))
    if bbq:
        with open_output(output, input.name, extension='.bbq') as f:
            for bibcode in bibcodes:
                f.write(bibcode)
                f.write("\n")
    with open_output(output, input.name, extension=".bib") as f:
        click.echo("Downloading bibliography to {0}".format(f.name))
        f.write(ads.ExportQuery(bibcodes).execute())
        click.echo("Wrote bibliography to {0}".format(f.name))

if __name__ == '__main__':
    main()
