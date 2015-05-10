r"""py-deps provides parsing the Python deps and generating graph data.

Initialize
----------

Cache the parsed dependencies into the ``py-deps.pickle``
on current working directory.This file format is
`pickle <https://docs.python.org/2.7/library/pickle.html>`_.::

    $ python
    >>> from py_deps import Package
    >>> pkg = Package('py-deps')


Change cache file
~~~~~~~~~~~~~~~~~

Use cache_name argument.::

    >>> pkg = Package('py-deps', cache_name='some-cache.name')


Override cache forcely
~~~~~~~~~~~~~~~~~~~~~~

Use ``update_force`` argument. (default: ``False``)::

    >>> pkg = Package('py-deps', update_force=True)


Generate rendering data
-----------------------

Supports follows currently.

* pretty print
* Linkdraw

Pretty print
~~~~~~~~~~~~

::

    >>> print(pkg.draw())
    py-deps -> [Sphinx, setuptools, pip, wheel, tox]
    setuptools -> [certifi, wincertstore, setuptools[ssl], pytest]
    pip -> [pytest, virtualenv, scripttest, mock, pytest, virtualenv,
     scripttest, mock]
    wheel -> [ed25519ll, keyring, argparse, pyxdg, jsonschema, pytest,
     coverage, pytest-cov]
    >>>

Linkdraw
~~~~~~~~

::

    >>> import json
    >>> json.loads(pkg.draw('linkdraw'))
    {u'descr': u'py-deps dependencies',
     u'lines': [{u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'py-deps', u'target': u'Sphinx', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'py-deps', u'target': u'setuptools', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'py-deps', u'target': u'pip', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'py-deps', u'target': u'wheel', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'py-deps', u'target': u'tox', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'setuptools', u'target': u'certifi', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'setuptools', u'target': u'wincertstore', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'setuptools', u'target': u'setuptools____ssl',
       u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'setuptools', u'target': u'pytest', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'pip', u'target': u'pytest', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'pip', u'target': u'virtualenv', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'pip', u'target': u'scripttest', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'pip', u'target': u'mock', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'pip', u'target': u'pytest', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'pip', u'target': u'virtualenv', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'pip', u'target': u'scripttest', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'pip', u'target': u'mock', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'wheel', u'target': u'ed25519ll', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'wheel', u'target': u'keyring', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'wheel', u'target': u'argparse', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'wheel', u'target': u'pyxdg', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'wheel', u'target': u'jsonschema', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'wheel', u'target': u'pytest', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'wheel', u'target': u'coverage', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'\u2192', u'link': u'',
       u'source': u'wheel', u'target': u'pytest-cov', u'width': u'1'}],
     u'nodes': [{u'color': u'', u'link': u'https://github.com/mkouhei/py-deps',
       u'name': u'py-deps', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'', u'name': u'Sphinx', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'https://bitbucket.org/pypa/setuptools',
       u'name': u'setuptools', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'https://pip.pypa.io/',
       u'name': u'pip', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'http://bitbucket.org/pypa/wheel/',
       u'name': u'wheel', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'', u'name': u'tox', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'', u'name': u'certifi', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'', u'name': u'wincertstore',
       u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'', u'name': u'setuptools____ssl',
       u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'', u'name': u'pytest', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'', u'name': u'virtualenv', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'', u'name': u'scripttest', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'', u'name': u'mock', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'', u'name': u'ed25519ll', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'', u'name': u'keyring', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'', u'name': u'argparse', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'', u'name': u'pyxdg', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'', u'name': u'jsonschema', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'', u'name': u'coverage', u'r': u'6'},
      {u'color': u'#5F9EA0', u'link': u'', u'name': u'pytest-cov',
       u'r': u'6'}],
     u'time': u'2015-05-08T03:52:59.542732'}

"""
from py_deps.deps import Package  # silence pyflakes
