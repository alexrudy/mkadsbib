``mkadsbib.py`` - Make bibliography from LaTeX Source
--------------------------------------------------

This is a quick script to make bibliographies from LaTeX source, using the NASA Astrophysics Data Service to generate the appropriate BibTeX file. Just use the NASA ADS bibcodes in your cite commands.

Quickstart
==========

If you've already set up access to the ADS API, using ``mkbib.py`` is as simple as::

    $ mkadsbib make mypaper.tex
    Extracted bibcodes from mypaper.aux
    Wrote bibliography to mypaper.bib

Note that you must have run LaTeX at least once to generate an ``.aux`` file which will contain the citations.

Installing ``mkbib.py``
=======================

Installation is as easy::

    pip install git+https://github.com/alexrudy/mkadsbib.git


(Coming to PyPI soon!)

Accessing the ADS API
=====================

In order to use the ADS API, you have to sign up for an API Key. Instructions for signing up for your API key are in the ``ads`` python module documentation: <https://github.com/andycasey/ads>

Extracting Bibcodes from LaTeX
==============================

To perform extraction only, run::

    $ mkadsbib extract mypaper.tex
    Extracted bibcodes from mypaper.tex into mypaper.bbq.


Querying a list of bibcodes
===========================

To query a list of bibcodes, generate a file with one bibcode per line,
then run::

    $ mkadsbib query mypaper.bbq
    Exported BibTeX to mypaper.bib.

