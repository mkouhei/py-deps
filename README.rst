==============
 About py-dep
==============

The ``py-dep`` provides parsing the dependencies of Python packages
and generating the metadata for graph.

The graph data is for `NetworkX <http://networkx.github.io/>`_, `Graphviz <http://www.graphviz.org/>`_, `blockdiag <http://blockdiag.com/>`_, `Linkdraw <https://github.com/mtoshi/linkdraw/wiki>`_, etc.

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
* NetworkX 1.9 over
  
Features
========

* Generating Linkdraw data (JSON and decoded JSON).
* Generating Networkx DiGraph object data.
* Cache the parsed dependencies.
* Searching packages from PyPI.

Known issue with the packages that depends on py-deps
=====================================================

The packages that depend on ``py-deps``; after that called "X" package, there is a known issue that fails to install using the `pip <https://pip.pypa.io/en/stable/>`_. This problem is caused by ``py-deps`` is a package that depends on the ``pip`` and `wheel <http://pythonwheels.com/>`_. When you install the "X" in the ``pip`` following exception occurs.::

  The AssertionError: Multiple .dist-info directories occures, because py-deps depends on pip, wheel.


Workaround
----------

The workaround for this problem is to use `setuptools <http://pythonhosted.org/setuptools/>`_ instead of ``pip``.

* You should use the ``easy_install`` command when you are installing the X from `PyPI <https://pypi.python.org/pypi>`_.
* Use the ``python setup.py install`` when you install from the source tree , such as repository.
* When you use the `Tox <https://testrun.org/tox/latest/>`_ in unit test , you should specify `install_command <https://testrun.org/tox/latest/example/basic.html?highlight=install_command#further-customizing-installation>`_ in ``[testenv]`` section of ``tox.ini``.::

    [testenv]
    install_command = easy_install {opts} {packages}

See also `pgraph <https://github.com/mkouhei/pgraph>`_ is already corresponding to the above-mentioned problems.
