``mkbib.py`` - Make bibliography from LaTeX Source
--------------------------------------------------

This is a quick script to make bibliographies from LaTeX source, using the NASA Astrophysics Data Service to generate the appropriate BibTeX file. Just use the NASA ADS bibcodes in your cite commands.

Quickstart
==========

If you've already set up access to the ADS API, using ``mkbib.py`` is as simple as::
    
    $ mkadsbib make mypaper.tex
    Extracted bibcodes from mypaper.aux
    Wrote bibliography to mypaper.bib
    

Installing ``mkbib.py``
=======================

Installation is as easy::
    
    pip install git+https://github.com/alexrudy/mkadsbib.git
    

(Coming to PyPI soon!)

Accessing the ADS API
=====================

In order to use the ADS API, you have to sign up for an API Key. Instructions for signing up for your API key are in the ``ads`` python module documentation: <https://github.com/andycasey/ads>


