==============
 About py-dep
==============

The ``py-dep`` provides parsing the dependencies of Python packages
and generating the metadata for graph.

The graph data is for `Graphviz <http://www.graphviz.org/>`_, `blockdiag <http://blockdiag.com/>`_, `Linkdraw <https://github.com/mtoshi/linkdraw/wiki>`_, etc.

Status
======

.. image:: https://secure.travis-ci.org/mkouhei/py-deps.png?branch=master
   :target: http://travis-ci.org/mkouhei/py-deps
.. image:: https://coveralls.io/repos/mkouhei/py-deps/badge.png?branch=master
   :target: https://coveralls.io/r/mkouhei/py-deps?branch=master
.. image:: https://img.shields.io/pypi/v/py-deps.svg
   :target: https://pypi.python.org/pypi/py-deps
.. image:: https://readthedocs.org/projects/py-deps/badge/?version=latest
   :target: https://readthedocs.org/projects/py-deps/?badge=latest
   :alt: Documentation Status

Requirements
============

* Python 2.7 over or Python 3.3 over or PyPy 2.4.0 over
* pip 1.5.6 or 6.1.1 over
* wheel 0.24.0 over

Features
========

* Generating Linkdraw data.
* Cache the parsed dependencies.

History
=======

0.2.0 (2015-05-10)
------------------

* Cache the parsed dependencies.
* Fixes setting the url of node and targets.

0.1.1 (2015-05-08)
------------------

* Fixes test data of pretty_print, linkdraw.

0.1.0 (2015-05-07)
------------------

* Supports generating linkdraw data.
* Supports pip 6.1.1 over.
* Supports wheel format for distribution.
* Adds unit tests.

0.0.1 (2015-04-29)
------------------

* First release


