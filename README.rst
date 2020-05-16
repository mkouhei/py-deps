==============
 About py-dep
==============

The ``py-dep`` provides parsing the dependencies of Python packages
and generating the metadata for graph.

The graph data is for `NetworkX <http://networkx.github.io/>`_, `Linkdraw <https://github.com/mtoshi/linkdraw/wiki>`_, etc.

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

* Python 3.8
* setuptools 46.1.0 over
* pip 20.0. over
* NetworkX 2.4 over
* pylibmc 1.6.1 over (optional)

Features
========

* Generating Linkdraw data (JSON and decoded JSON).
* Generating Networkx DiGraph object data.
* Cache the parsed dependencies.
* Searching packages from PyPI.

