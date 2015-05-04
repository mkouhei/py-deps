"""py-deps provides parsing the Python deps and generating graph data.

Initialize
----------

::

    $ python
    >>> from py_deps import Package
    >>> pkg = Package('py-deps')

Pretty print
------------

::

    >>> pkg.draw()
    py-deps -> [setuptools, pip, wheel]
    setuptools -> [certifi, wincertstore, setuptools[ssl], pytest]
    pip -> [pytest, virtualenv, scripttest, mock, pytest,
     virtualenv, scripttest, mock]
    wheel -> [ed25519ll, keyring, argparse, pyxdg, jsonschema,
     pytest, coverage, pytest-cov]
    >>>

"""
from py_deps.deps import Package  # silence pyflakes
