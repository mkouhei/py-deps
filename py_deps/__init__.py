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

Show latest version
-------------------

Retrieve latest package from PyPI.::

    $ python
    >>> from py_deps.deps import latest_version
    >>> latest_version('deps')
    '0.1.0'


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

    >>> pkg = Package('py-deps', version='0.5.5')
    >>> pkg.version
    0.5.5


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
    py-deps -> [networkx, pip, setuptools, wheel]
    networkx -> [decorator]
    >>>

Linkdraw
~~~~~~~~

::

    >>> import pprint
    >>> pp = pprint.PrettyPrinter(width=120)
    >>> pp.pprint(pkg.draw('linkdraw'))
    {'descr': 'py-deps dependencies',
     'lines': [{'color': '#d1e0fa', 'descr': '->', 'link': '', 'source': 'py-deps', 'target': 'networkx', 'width': '1'},
               {'color': '#a4c1f4', 'descr': '->', 'link': '', 'source': 'networkx', 'target': 'decorator', 'width': '1'},
               {'color': '#d1e0fa', 'descr': '->', 'link': '', 'source': 'py-deps', 'target': 'pip', 'width': '1'},
               {'color': '#d1e0fa', 'descr': '->', 'link': '', 'source': 'py-deps', 'target': 'setuptools', 'width': '1'},
               {'color': '#d1e0fa', 'descr': '->', 'link': '', 'source': 'py-deps', 'target': 'wheel', 'width': '1'}],
     'nodes': [{'color': '#d1e0fa',
                'depth': 0,
                'link': 'https://github.com/mkouhei/py-deps',
                'name': 'py-deps',
                'r': '6',
                'version': '0.5.5'},
               {'color': '#a4c1f4',
                'depth': 1,
                'link': 'http://networkx.github.io/',
                'name': 'networkx',
                'r': '6',
                'version': '2.4'},
               {'color': '#76a1ef',
                'depth': 2,
                'link': 'https://github.com/micheles/decorator',
                'name': 'decorator',
                'r': '6',
                'version': '4.4.2'},
               {'color': '#a4c1f4', 'depth': 1, 'link': 'https://pip.pypa.io/', 'name': 'pip', 'r': '6', 'version': '20.1'},
               {'color': '#a4c1f4',
                'depth': 1,
                'link': 'https://github.com/pypa/setuptools',
                'name': 'setuptools',
                'r': '6',
                'version': '46.3.1'},
               {'color': '#a4c1f4',
                'depth': 1,
                'link': 'https://github.com/pypa/wheel',
                'name': 'wheel',
                'r': '6',
                'version': '0.34.2'}],
     'time': '2020-05-16T14:06:52.790139'}



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

    >>> from py_deps.cache import backend
    >>> backend().list_data()
    {('py-deps', '0.5.5'): [py-deps]}
     (snip)}

Read the cached package with ``read_data`` method of :class:`Container`.
This method returns :class:`Package.traced_chain`.

    >>> Container().read_data(('py-deps', '0.5.5'))
    [py-deps]


"""
from py_deps.deps import Package
from py_deps.cache import Container
