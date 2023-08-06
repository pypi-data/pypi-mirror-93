Installing HyperNetX
====================

The HyperNetX library provides classes and methods for the analysis 
and visualization of complex network data. HyperNetX uses data structures 
designed to represent set systems containing nested data and/or multi-way 
relationships. The library generalizes traditional graph metrics to hypergraphs.

HypernetX was developed by the Pacific Northwest National Laboratory for the 
Hypernets project as part of its High Performance Data Analytics (HPDA) program. 
PNNL is operated by Battelle Memorial Institute under Contract DE-AC05-76RL01830.

* Principle Developer and Designer: Brenda Praggastis
* Graphics Developer and Designer: Dustin Arendt
* Program Manager: Cliff Joslyn, Brian Kritzstein
* Mathematics, methods, and algorithms: Sinan Aksoy, Dustin Arendt, Cliff Joslyn, Brenda Praggastis, and Emilie Purvine

The current version is a beta version intended for users to test and report bugs. 
We are actively testing and would be grateful for your feedback.
This version is not available on Github, but is available in PyPI using
```
pip install hnxbeta
```
Expect changes in both class names and methods as 
many of the requirements demanded of the library are worked out. 

For questions and comments you may contact the developers directly at:   
	hypernetx@pnnl.gov

To install in an Anaconda environment
-------------------------------------

	>>> conda create -n <env name> python=3.8
	>>> source activate <env name> 

To install in a virtualenv environment
--------------------------------------

	>>> virtualenv --python=<path to python 3.8 executable> <path to env name>

This will create a virtual environment in the specified location using
the specified python executable. For example:

	>>> virtualenv --python=C:\Anaconda3\python.exe hnx

This will create a virtual environment in .\hnx using the python
that comes with Anaconda3.

	>>> <path to env name>\Scripts\activate<file extension>

If you are running in Windows PowerShell use <file extension>=.ps1

If you are running in Windows Command Prompt use <file extension>=.bat

Otherwise use <file extension>=NULL (no file extension).

Once activated continue to follow the installation instructions below.

System Requirements for using C++ backend
-----------------------------------------
The hnxbeta version has C++ support availablefrom the NWHypergraph library. 
This library is still in development and will be updated frequently on PyPI.
At present it is only available for OSX and Centos7.
Mac users will need to brew install tbb and upgrade their gcc to 10.2.0
This can be done with `brew install gcc@10`  or `brew upgrade gcc`
To install NWHypergraph: pip install nwhy

Install hnxbeta using Pip
-----------------

For a minimal installation using wheel files available on PyPI:

	>>> pip install hnxbeta

For an editable installation with tutorials and testing using this package: 

	>>> cd hnxbeta
    >>> pip install -e .['all']

License
-------

Released under the 3-Clause BSD license (see :ref:`license`)



