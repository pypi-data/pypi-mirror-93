#! /usr/bin/env python
"""A template."""

import codecs
import os

from setuptools import find_packages, setup

# get __version__ from _version.py
ver_file = os.path.join('deep_logic', '_version.py')
with open(ver_file) as f:
    exec(f.read())

DISTNAME = 'deep-logic'
DESCRIPTION = 'Deep logic: Interpretable neural networks in Python.'
with codecs.open('README.rst') as f:
    LONG_DESCRIPTION = f.read()
MAINTAINER = 'P. Barbiero'
MAINTAINER_EMAIL = 'barbiero@tutanota.com'
URL = 'https://github.com/pietrobarbiero/deep-logic'
LICENSE = 'Apache 2.0'
DOWNLOAD_URL = 'https://github.com/pietrobarbiero/deep-logic'
VERSION = __version__
INSTALL_REQUIRES = ['numpy', 'torch', 'sympy']
CLASSIFIERS = ['Intended Audience :: Science/Research',
               'Intended Audience :: Developers',
               'License :: OSI Approved',
               'Programming Language :: Python',
               'Topic :: Software Development',
               'Topic :: Scientific/Engineering',
               'Operating System :: Microsoft :: Windows',
               'Operating System :: POSIX',
               'Operating System :: Unix',
               'Operating System :: MacOS',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6',
               'Programming Language :: Python :: 3.7']
EXTRAS_REQUIRE = {
    'tests': [
        'pytest',
        'pytest-cov'],
    'docs': [
        'sphinx',
        'sphinx-gallery',
        'sphinx_rtd_theme',
        'numpydoc',
        'matplotlib'
    ]
}

setup(name=DISTNAME,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      contributors=['HekpoMaH'],
      description=DESCRIPTION,
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      long_description_content_type='text/x-rst',
      long_description=LONG_DESCRIPTION,
      zip_safe=False,  # the package can run out of an .egg file
      classifiers=CLASSIFIERS,
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE)
