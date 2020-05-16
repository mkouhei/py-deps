# -*- coding: utf-8 -*-
"""py_deps.deps module."""
import os
import pkg_resources
import sys
import subprocess
import tempfile
from glob import glob
import xmlrpc.client as xmlrpclib
from pip._internal.utils.misc import rmtree
from pip._internal.commands.show import search_packages_info
from py_deps import graph, cache
from py_deps.exceptions import BackendFailure


#: suffix of temporary directory name
SUFFIX = '-py_deps'
PYPI_URL = 'https://pypi.python.org/pypi'


def u2h(name):
    """Change underscore to hyphen of package name.

    :rtype: str
    :return: string replaced underscore with hyphen

    :param str name: package name
    """
    return name.replace('_', '-')


def search(pkg_name, exactly=False):
    """Search package.

    :rtype: list
    :return: search packages

    :param str pkg_name: package name.
    :param bool exactly: exactly match only.
    """
    try:
        client = xmlrpclib.ServerProxy(PYPI_URL)
        result = client.search({'name': pkg_name})
        # pylint: disable=undefined-variable
    except (TimeoutError,
            ConnectionRefusedError,
            xmlrpclib.ProtocolError) as exc:
        raise BackendFailure(exc)
    if exactly:
        result = [pkg for pkg in result
                  if u2h(pkg.get('name')) == u2h(pkg_name)]
    return result


def latest_version(pkg_name):
    """Retrieve latest version.

    :rtype: str
    :return: latest version

    :param str pkg_name: package name.
    """
    try:
        client = xmlrpclib.ServerProxy(PYPI_URL)
        package_releases = client.package_releases(pkg_name)
        # pylint: disable=undefined-variable
    except (TimeoutError,
            ConnectionRefusedError,
            xmlrpclib.ProtocolError) as exc:
        raise BackendFailure(exc)
    if package_releases:
        result = package_releases[0]
    else:
        result = ''
    return result


def create_nodes(package_names, depth=0):
    """Show information about installed package."""
    nodes = list()
    results = search_packages_info(package_names)
    try:
        for _, dist in enumerate(results):
            node = Node(
                dist.get('name'),
                dist.get('version'),
                url=dist.get('home-page'),
                requires=dist.get('requires'),
                depth=depth
            )
            if len(dist.get('requires')) > 0:
                _nodes = create_nodes(dist.get('requires'), node.depth + 1)
                node.targets += _nodes
            nodes.append(node)
    except StopIteration:
        pass
    finally:
        return nodes  # pylint: disable=lost-exception


# pylint: disable=too-many-instance-attributes
class Package:
    """Package class."""

    #: index_url
    index_url = 'https://pypi.python.org/simple'
    pip_command = 'pip'

    def __init__(self, name, version=None, update_force=False, **kwargs):
        """Initialize to parsing dependencies of package."""
        #: package name
        self.name = name
        self.version = version
        self._cache = cache.backend(**kwargs)
        self.container = self._cache.container
        self.tempdir = tempfile.mkdtemp(suffix=SUFFIX)

        pkg_ver = (self.name, self.version)
        if self._cache.read_data(pkg_ver) is None or update_force:
            self.install()
            self.__load_path()
            self.requires = create_nodes([name])
            self.__restore_path()
            self.traced_chain = self.requires
            self._cache.store_data(pkg_ver, self.traced_chain)
        else:
            self.traced_chain = self._cache.read_data(pkg_ver)
        self.cleanup()

    # pylint: disable=protected-access
    def __load_path(self):
        sys.path.append(self.tempdir)
        pkg_resources.working_set = pkg_resources.WorkingSet._build_master()

    # pylint: disable=protected-access
    def __restore_path(self):
        if self.tempdir in sys.path:
            sys.path.remove(self.tempdir)
        pkg_resources.working_set = pkg_resources.WorkingSet._build_master()

    def cleanup(self, alldir=False):
        """Cleanup temporary build directory.

        :param bool alldir: Remove all temporary directories. (default: False)

        :rtype: None
        """
        if alldir:
            [rmtree(tempdir, ignore_errors=True)
             for tempdir in
             glob("{0}/tmp*{1}".format(os.path.dirname(self.tempdir),
                                       SUFFIX))]
        else:
            rmtree(self.tempdir, ignore_errors=True)

    def install(self):
        """Install packages to build_dir."""
        if self.version is None:
            cmdline = (f'{self.pip_command} install --isolated '
                       f'-t {self.tempdir} {self.name}')
        else:
            cmdline = (f'{self.pip_command} install --isolated '
                       f'-t {self.tempdir} {self.name}=={self.version}')
        subprocess.run(cmdline.split(), check=True)

    def draw(self, draw_type=None, link_prefix=None):
        """Generate drawing data.

        :param str draw_type: [dot|blockdiag|linkdraw]
        """
        return graph.router(self, draw_type=draw_type, link_prefix=link_prefix)


class Node:
    """Node object class."""

    # pylint: disable=too-many-arguments
    def __init__(self, name, version=None, url=None, requires=None, depth=0):
        """Initialize."""
        #: name
        self.name = name
        #: version
        self.version = version
        #: project url
        self.url = url
        #: requires
        self.requires = requires
        #: targets
        self.targets = []
        #: test targets
        self.test_targets = []
        #: base dependency depth level
        self.depth = depth

    def __repr__(self):
        """Return Node object name."""
        return str(self.name)
