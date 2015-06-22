# -*- coding: utf-8 -*-
"""py_deps.cache module."""
import os.path
import pickle


#: default cache file name
DEFAULT_CACHE_NAME = 'py-deps.pickle'


def backend(backend_type=None, cache_name=None):
    """Specify cache backend."""
    if backend_type == 'memcached':
        pass
    else:
        # default Pickle
        return Pickle(cache_name=cache_name)


class Container(object):

    """Package container class."""

    def __init__(self, cache_name=None):
        """Initialize."""
        self.cache_name = cache_name
        self.container = {}
        self.load_cache()

    def load_cache(self):
        """Load cache."""
        pass

    def save_cache(self):
        """Save cache."""
        pass

    def read_data(self, key):
        """Read traced_chain data.

        :rtype: list
        :return: dependency chain list

        :param tuple key: package name, version
        """
        return self.container.get(key)

    def store_data(self, key, data):
        """Store traced_chain data.

        :param tuple key: package name, version
        :param list data: traced dependency chain data
        """
        self.container[key] = data
        self.save_cache()

    def list_data(self):
        """Return dictionary stored package metadata.

        :rtype: dict
        :return: packages metadata
        """
        return self.container


class Pickle(Container):

    """Cache backend is Pickle."""

    #: default cache file name
    default_cache_name = 'py-deps.pickle'

    def __init__(self, cache_name=None):
        """Initialize."""
        if cache_name is None:
            cache_name = self.default_cache_name
        super(Pickle, self).__init__(cache_name)

    def load_cache(self):
        """Load cache file."""
        if os.path.isfile(self.cache_name):
            with open(self.cache_name, 'rb') as fobj:
                self.container = pickle.load(fobj)

    def save_cache(self):
        """Save cache file."""
        with open(self.cache_name, 'wb') as fobj:
            pickle.dump(self.container, fobj)
