from __future__ import with_statement

from setuptools import setup

import mkadsbib

mkadsbib_classifiers = [
    "Programming Language :: Python :: 3",
]

setup(name="mkadsbib",
      version=mkadsbib.__version__,
      author="Alexander Rudy",
      author_email="arrudy@ucsc.edu",
      url="http://pypi.python.org/pypi/mkadsbib/",
      py_modules=["mkadsbib"],
      install_requires=['click', 'ads'],
      description="Make bibliographies from ADS Bibcodes",
      long_description="Really, make bibliographies from ADS Bibcodes",
      license="MIT",
      classifiers=mkadsbib_classifiers,
      entry_points={
          'console_scripts': ['mkadsbib = mkadsbib.main']
      }
      )