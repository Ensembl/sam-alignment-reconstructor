Overview
########

This package is design to reconstruct pairwise alignments from SAM files using the CIGAR string and MD:Z tag

It can be used as a standalone command line tool, or as a library when get the three elements above.

Usage
#####

To install the package, enable the virtual environment where it's going to be used and run

::

  $ pip install sam-alignment-reconstructor

Developing
##########

To prepare the environment for developing the library, create a virtual environment, go to project root and then run:

::

  $ pip install -e .[dev]

Testing
#######
The recommended way is to test using detox.
This allows for testing in all the supported python versions using virtual environments effortlessly.
To use, install it, then run in the project root:

::

  $ pip install detox
  $ detox

Alternatively, testing can be done in the same environment as the dev one by installing it's dependencies, then running pytest:

::

  $ pip install -e .[test]
  $ python -m pytest -s
