r"""py-deps provides parsing the Python deps and generating graph data.

Search packages
---------------

Search packages from PyPI.::

    $ python
    >>> from py_deps.deps import search
    >>> search('deps')
    [{'_pypi_ordering': False,
      'name': 'anybox.recipe.sysdeps',
      'summary': 'A buildout recipe to check system dependencies',
      'version': '0.5'},
     {'_pypi_ordering': False,
      'name': 'appdynamics-bindeps-linux-x64',
      'summary': 'Dependencies for AppDynamics Python agent',
      'version': '4.0.5.0'},
     {'_pypi_ordering': False,
      'name': 'appdynamics-bindeps-linux-x86',
      'summary': 'Dependencies for AppDynamics Python agent',
      'version': '4.0.5.0'},
     {'_pypi_ordering': False,
      'name': 'appdynamics-bindeps-osx-x64',
      'summary': 'Dependencies for AppDynamics Python agent',
      'version': '4.0.5.0'},
     {'_pypi_ordering': False,
      'name': 'deps',
      'summary': 'deps discovers your Python dependencies',
      'version': '0.1.0'},
     {'_pypi_ordering': False,
      'name': 'gtkeggdeps',
      'summary': 'Interactive egg dependency browser',
      'version': '0.0.7'},
     {'_pypi_ordering': False,
      'name': 'htmldeps',
      'summary': 'Expand CSS and javascript dependency links in HTML',
      'version': '1.2.1'},
     {'_pypi_ordering': False,
      'name': 'py-deps',
      'summary': 'parsing the Python deps and generating graph data',
      'version': '0.3.0'},
     {'_pypi_ordering': False,
      'name': 'pydeps',
      'summary': 'Display module dependencies',
      'version': '1.2.1'},
     {'_pypi_ordering': False,
      'name': 'runestone-test-deps',
      'summary': 'This is dependencies for RSI',
      'version': '0.1'},
     {'_pypi_ordering': False,
      'name': 'tl.eggdeps',
      'summary': 'Compute a dependency graph between active Python eggs.',
      'version': '0.4'},
     {'_pypi_ordering': False,
      'name': 'tt.eggdeps',
      'summary': 'Compute a dependency graph between active Python eggs.',
      'version': '0.5'}]


Initialize
----------

Cache the parsed dependencies into the ``py-deps.pickle``
on current working directory.This file format is
`pickle <https://docs.python.org/2.7/library/pickle.html>`_.::

    $ python
    >>> from py_deps import Package
    >>> pkg = Package('py-deps')

py-deps retrieve latest version from PyPI
without ``version`` argument as above.
Specify version use version argument.::

    >>> pkg = Package('py-deps', version='0.3.0')
    >>> pkg.version
    0.3.0


Change cache file
~~~~~~~~~~~~~~~~~

Use cache_name argument.::

    >>> pkg = Package('py-deps', cache_name='some-cache.name')


Override cache forcely
~~~~~~~~~~~~~~~~~~~~~~

Use ``update_force`` argument. (default: ``False``)::

    >>> pkg = Package('py-deps', update_force=True)


Changes the cache backend to Memcached
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Installing libmemcached-dev package and pylibmc.::

    $ sudo apt-get install libmemcached-dev
    $ . /path/to/venv/bin/activate
    (venv)$ cd /path/to/py-deps
    (venv)$ python setup.py memcache

Use ``servers`` argument. The argment syntax follows pylibmc.Client.::

    >>> pkg = Package('py-deps', servers=['127.0.0.1:11211'])


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
     u'lines': [{u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'py-deps', u'target': u'Sphinx', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'py-deps', u'target': u'setuptools', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'py-deps', u'target': u'pip', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'py-deps', u'target': u'wheel', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'py-deps', u'target': u'tox', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'setuptools', u'target': u'certifi', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'setuptools', u'target': u'wincertstore', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'setuptools', u'target': u'setuptools____ssl',
       u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'setuptools', u'target': u'pytest', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'pip', u'target': u'pytest', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'pip', u'target': u'virtualenv', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'pip', u'target': u'scripttest', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'pip', u'target': u'mock', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'pip', u'target': u'pytest', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'pip', u'target': u'virtualenv', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'pip', u'target': u'scripttest', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'pip', u'target': u'mock', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'wheel', u'target': u'ed25519ll', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'wheel', u'target': u'keyring', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'wheel', u'target': u'argparse', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'wheel', u'target': u'pyxdg', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'wheel', u'target': u'jsonschema', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'wheel', u'target': u'pytest', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
       u'source': u'wheel', u'target': u'coverage', u'width': u'1'},
      {u'color': u'#5F9EA0', u'descr': u'->', u'link': u'',
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


See also `How to use linkdraw
<https://github.com/mtoshi/linkdraw/wiki#how-to-use-linkdraw>`_.


NetworkX
~~~~~~~~

::

    >>> pkg.draw('networkx')
    >>> <networkx.classes.digraph.DiGraph at 0x7fbe2311dbd0>


Check cache
-----------

Stores parsed dependency metadata to pickles data file.
The file name is ``py-deps.pickle`` in default.

Listing cached data with the ``list_data`` method of :class:`Container`.::

    >>> from py_deps import Container
    >>> Container().list_data()
    {'py-deps': [py-deps, setuptools, pip, wheel, networkx, decorator],
     (snip)}

Read the cached package with ``read_data`` method of :class:`Container`.
This method returns :class:`Package.traced_chain`.

    >>> Container().read_data(('py-deps', '0.3.0'))
    [py-deps, setuptools, pip, wheel, networkx, decorator]


"""
from py_deps.deps import Package  # silence pyflakes
from py_deps.cache import Container  # silence pyflakes
