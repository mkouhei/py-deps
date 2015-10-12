# -*- coding: utf-8 -*-
"""py_deps.cache module."""
import os.path
import pickle
try:
    import pylibmc
except ImportError:
    pass


def backend(**kwargs):
    """Specify cache backend.

    :rtype: :class:`py_deps.cache.Container`
    :return: Pickle object or Memcached object.

    :param **kwargs: parameters

    servers
        Memcached servers (required in Memcached)

        Required when Memcached. Using Pickle in default without ``servers``.

    username
        Memcached SASL username (optional)

    password
        Memcached SASL password (optional)

    cache_name
        Pickle filename (default, optional)
    """
    if kwargs.get('servers'):
        return Memcached(kwargs.get('servers'),
                         username=kwargs.get('username'),
                         password=kwargs.get('password'),
                         behaviors=kwargs.get('behaviors'))
    else:
        # default Pickle
        return Pickle(cache_name=kwargs.get('cache_name'))


class Container(object):
    """Package container class."""

    def __init__(self, cache_name=None):
        """Initialize."""
        self.cache_name = cache_name
        self.container = {}

    def store_data(self, key, data):
        """store traced_chain data."""
        pass

    def read_data(self, key):
        """Read traced_chain data.

        :rtype: list
        :return: dependency chain list

        :param tuple key: package name, version
        """
        return self.container.get(key)

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

    def store_data(self, key, data):
        """Store traced_chain data.

        :param tuple key: package name, version
        :param list data: traced dependency chain data
        """
        self.container[key] = data
        self.save_cache()


class Memcached(Container):
    """Cache backend is Memecached."""

    def __init__(self, servers=None,
                 username=None,
                 password=None,
                 behaviors=None):
        """Initialize."""
        super(Memcached, self).__init__()
        if username and password:
            self.container = pylibmc.Client(servers,
                                            binary=True,
                                            username=username,
                                            password=password)
        else:
            self.container = pylibmc.Client(servers,
                                            binary=True)

    def store_data(self, key, data):
        """Store traced_chain data.

        :param tuple key: package name, version
        :param list data: traced dependency chain data
        """
        # pylint: disable=no-member
        self.container.set('{0} {1}'.format(*key), data)

    def read_data(self, key):
        """Read traced_chain data.

        :rtype: list
        :return: dependency chain list

        :param tuple key: package name, version
        """
        return self.container.get('{0} {1}'.format(*key))
