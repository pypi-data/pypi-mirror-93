from setuptools import setup
import sys
import os.path

__version__ = '0.1.3'

if sys.version_info < (3, 8):
    sys.exit('HyperNetX requires Python 3.8 or later.')

setup(
    name='hnxbeta',
    packages=['hypernetx',
              'hypernetx.algorithms',
              'hypernetx.classes',
              'hypernetx.drawing',
              'hypernetx.utils'],
    version=__version__,
    author="Brenda Praggastis, Dustin Arendt, Emilie Purvine, Cliff Joslyn",
    author_email="hypernetx@pnnl.gov",
    url='https://github.com/pnnl/HyperNetX',
    description='HyperNetX is a Python library for the creation and study of hypergraphs.',
    install_requires=['networkx>=2.2,<3.0',
                      'numpy>=1.15.0,<2.0',
                      'scipy>=1.1.0,<2.0',
                      'matplotlib>3.0',
                      'scikit-learn>=0.20.0',
                      'tbb',
                      ],
    license='3-Clause BSD license',
    long_description='''
    Hnxbeta is a development version of HyperNetX 
    intended for super users to test and give feedback. 
    Please install in a virtual environment and send comments and bug reports to
    hypernetx@pnnl.gov

    The HyperNetX library provides classes and methods for complex network data.
    HyperNetX uses data structures designed to represent set systems containing
    nested data and/or multi-way relationships. The library generalizes traditional
    graph metrics to hypergraphs.

    Hnxbeta has C++ support available from the NWHypergraph library. 
    This library is still in development and will be updated frequently on PyPI.
    At present it is only available for OSX and Centos7.
    Mac users will need to `brew install tbb` and upgrade their gcc to 10.2.0
    This can be done with `brew install gcc@10`  or `brew upgrade gcc`
    To install NWHypergraph: `pip install nwhy`
    ''',
    extras_require={
        'testing': ['pytest>=4.0'],
        'tutorials': ['jupyter>=1.0', 'pandas>=0.23'],
        'all': ['pytest>=4.0', 'jupyter>=1.0', 'pandas>=0.23']
    }
)

# This is a beta version of HyperNetX intended for users to test and give feedback. Please install in a virtual environment.
