r"""py-deps provides parsing the Python deps and generating graph data.

Initialize
----------

::

    $ python
    >>> from py_deps import Package
    >>> pkg = Package('py-deps')

Pretty print
------------

::

    >>> print(pkg.draw())
    py-deps -> [setuptools, pip, wheel]
    setuptools -> [certifi, wincertstore, setuptools[ssl], pytest]
    pip -> [pytest, virtualenv, scripttest, mock, pytest,
     virtualenv, scripttest, mock]
    wheel -> [ed25519ll, keyring, argparse, pyxdg, jsonschema,
     pytest, coverage, pytest-cov]
    >>>

Linkdraw
--------

::

    >>> import json
    >>> json.loads(pkg.draw('linkdraw'))
    {"nodes": [
      {"color": "", "r": "6", "link": "", "name": "py-deps"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "setuptools"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "pip"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "wheel"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "certifi"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "wincertstore"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "setuptools____ssl"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "pytest"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "virtualenv"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "scripttest"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "mock"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "ed25519ll"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "keyring"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "argparse"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "pyxdg"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "jsonschema"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "coverage"},
      {"color": "#5F9EA0", "r": "6", "link": "", "name": "pytest-cov"}],
    "lines": [
      {"source": "py-deps", "link": "", "target": "setuptools",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "py-deps", "link": "", "target": "pip",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "py-deps", "link": "", "target": "wheel",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "setuptools", "link": "", "target": "certifi",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "setuptools", "link": "", "target": "wincertstore",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "setuptools", "link": "", "target": "setuptools____ssl",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "setuptools", "link": "", "target": "pytest",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "pip", "link": "", "target": "pytest",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "pip", "link": "", "target": "virtualenv",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "pip", "link": "", "target": "scripttest",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "pip", "link": "", "target": "mock",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "pip", "link": "", "target": "pytest",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "pip", "link": "", "target": "virtualenv",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "pip", "link": "", "target": "scripttest",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "pip", "link": "", "target": "mock",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "wheel", "link": "", "target": "ed25519ll",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "wheel", "link": "", "target": "keyring",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "wheel", "link": "", "target": "argparse",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "wheel", "link": "", "target": "pyxdg",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "wheel", "link": "", "target": "jsonschema",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "wheel", "link": "", "target": "pytest",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "wheel", "link": "", "target": "coverage",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"},
      {"source": "wheel", "link": "", "target": "pytest-cov",
       "descr": "\u2192", "width": "1", "color": "#5F9EA0"}],
    "descr": "py-deps dependencies", "time": "2015-05-05T23:52:53.198572"}

"""
from py_deps.deps import Package  # silence pyflakes
