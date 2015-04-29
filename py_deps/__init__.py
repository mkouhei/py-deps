"""py-deps provides parsing the Python deps and generating graph data.

Initialize.
-----------

::
    $ python
    >>> from py_deps import Package
    >>> pkg = Package('py-deps')
    >>> pkg.download()
    >>> pkg.list_requires()
    >>> pkg.cleanup()

"""
from py_deps.deps import Package  # silence pyflakes
