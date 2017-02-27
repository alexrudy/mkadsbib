#!/usr/bin/env python3

import click
import os
import re

@click.group()
@click.option("--sandbox/--no-sandbox", default=False, help="Query against the ads sandbox.")
def main(sandbox):
    """Make bibliographies"""
    global ads
    if sandbox:
        import ads.sandbox as ads
    else:
        import ads
    
@main.command()
@click.argument('input', type=click.File(mode='r'))
def transform(input):
    """Transform a list of bibcodes to bib entries."""
    bibcodes = [line for line in input]
    output = "{0}.bib".format(os.path.splitext(input.name)[0])
    with open(output, 'w') as f:
        f.write(ads.ExportQuery(bibcodes).execute())

def parse(lines):
    """Parse a line."""
    for line in lines:
        citation = re.match(r'\\citation\{([\S]+)\}', line)
        if citation:
            yield citation.group(1)
        fileinput = re.match(r'\\@?input\{([\S]+)\}', line)
        if fileinput:
            print("Reading {0}".format(fileinput.group(1)))
            with open(fileinput.group(1), 'r') as subfile:
                yield from parse(subfile)

@main.command()
@click.option("-o", "--output", default=None, help="Output file name.")
@click.argument('input', type=click.File(mode='r'))
def extract(input, output):
    """Extract citations"""
    if output is None:
        output = "{0}.bbq".format(os.path.splitext(input.name)[0])
    with open(output, 'w') as f:
        for citation in parse(input):
            f.write(citation)
            f.write("\n")

if __name__ == '__main__':
    main()