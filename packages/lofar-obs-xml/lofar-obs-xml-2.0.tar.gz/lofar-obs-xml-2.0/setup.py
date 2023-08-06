#!/usr/bin/env python

from setuptools import setup
from momxml import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(name='lofar-obs-xml',
      version      = __version__,
      description  = 'Generate XML file with LOFAR system validation observations',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author       = 'Michiel Brentjens',
      author_email = 'brentjens@astron.nl',
      url          = 'https://github.com/brentjens/lofar-obs-xml',
      packages     = ['momxml', 'lofarobsxml'],
      requires     = ['ephem'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      scripts      = ['genvalobs'],
     )
