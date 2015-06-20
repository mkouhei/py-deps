# -*- coding: utf-8 -*-
"""py_deps.cache module."""
import os.path
import pickle


#: default cache file name
DEFAULT_CACHE_NAME = 'py-deps.pickle'


class Container(object):

    """Package container class."""

    def __init__(self, cache_name=None):
        """Initialize."""
        if cache_name:
            self.cache_name = cache_name
        else:
            self.cache_name = DEFAULT_CACHE_NAME
        self.container = {}
        self.load_cache()

    def load_cache(self):
        """Load cache file."""
        if os.path.isfile(self.cache_name):
            with open(self.cache_name, 'rb') as fobj:
                self.container = pickle.load(fobj)

    def save_cache(self):
        """Save cache file."""
        with open(self.cache_name, 'wb') as fobj:
            pickle.dump(self.container, fobj)

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
