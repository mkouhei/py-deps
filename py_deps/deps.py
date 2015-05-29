# -*- coding: utf-8 -*-
"""py_deps.deps module."""
import sys
import os
import tempfile
import re
import pip
import wheel.util
from glob import glob
from pip.req import RequirementSet, InstallRequirement
from pip.locations import src_prefix
from pip.download import PipSession
from pip.index import PackageFinder
from pkg_resources import PathMetadata, Distribution
import pickle
import logging
from py_deps import graph
if pip.__version__ >= '6.0.0':
    from pip.utils import rmtree
else:
    from pip.util import rmtree
if sys.version_info > (3, 0):
    import xmlrpc.client as xmlrpclib
else:
    import xmlrpclib


#: suffix of temporary directory name
SUFFIX = '-py_deps'
#: default cache file name
DEFAULT_CACHE_NAME = 'py-deps.pickle'
PYPI_URL = 'https://pypi.python.org/pypi'


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

        :param str key: package name
        """
        return self.container.get(key)

    def store_data(self, key, data):
        """Store traced_chain data.

        :param str key: package name
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


class Package(object):

    """Package class."""

    #: index_url
    index_url = 'https://pypi.python.org/simple'

    def __init__(self, name, cache_name=None, update_force=False):
        """Initialize to parsing dependencies of package."""
        #: package name
        self.name = name
        cache = Container(cache_name)
        self.container = cache.container
        self.tempdir = tempfile.mkdtemp(suffix=SUFFIX)

        if cache.read_data(name) is None or update_force:

            self.finder = PackageFinder(find_links=[],
                                        index_urls=[self.index_url],
                                        session=PipSession())
            self.reqset = RequirementSet(build_dir=self.tempdir,
                                         src_dir=src_prefix,
                                         download_dir=None,
                                         upgrade=True,
                                         ignore_installed=True,
                                         session=PipSession())

            req = InstallRequirement.from_line(name,
                                               comes_from=None)
            self.reqset.add_requirement(req)
            self.requires = []
            self.traced_chain = []
            self.trace_chain()
            cache.store_data(name, self.traced_chain)
        else:
            self.traced_chain = cache.read_data(name)
            self.cleanup()

    @classmethod
    def search(cls, pkg_name, exactly=False):
        """Search package.

        :rtype: list
        :return: search packages

        :param str pkg_name: package name.
        :param bool exactly: exactly match only.
        """
        client = xmlrpclib.ServerProxy(PYPI_URL)
        result = client.search({'name': pkg_name})
        if exactly:
            return [pkg for pkg in result
                    if u2h(pkg.get('name')) == u2h(pkg_name)]
        else:
            return result

    def cleanup(self, alldir=False):
        """Cleanup temporary build directory.

        :param bool alldir: Remove all temporary directories. (default: False)

        :rtype: None
        """
        if alldir:
            for tempdir in glob("%s/tmp*%s" % (os.path.dirname(self.tempdir),
                                               SUFFIX)):
                rmtree(tempdir, ignore_errors=True)
        else:
            rmtree(self.tempdir, ignore_errors=True)

    def _download(self):
        """Download packages to build_dir.

        This method does not download requires recursively.
        """
        try:
            self.reqset.prepare_files(self.finder)
        except pip.exceptions.DistributionNotFound:
            _type, _val, _tb = sys.exc_info()
            msg = ("%s\n  CODE: %s\n  LINE: %s\n  NAME: %s\n  MSG : %s" %
                   (_type,
                    _tb.tb_frame.f_code.co_filename,
                    _tb.tb_lineno,
                    _tb.tb_frame.f_code.co_name,
                    _val))
            logging.warning(msg)

    def _list_requires(self):
        """Listing requires object or dict object.

        :rtype: list
        :return: requires object or dict object
        """
        if not self.requires:
            self._download()
            self._collect_requires()
            self.cleanup()
        return self.requires

    def trace_chain(self, pkg_name=None):
        """Trace dependency chain.

        :param str pkg_name: package name
        """
        if pkg_name is None:
            pkg_name = self.name
        pkg = [req for req in self._list_requires()
               if u2h(req.name) == u2h(pkg_name)]
        if len(pkg) == 0:
            return
        if pkg[0] not in self.traced_chain:
            self.traced_chain.append(pkg[0])
        if len(pkg[0].targets) > 0:
            for target in pkg[0].targets:
                self.trace_chain(target.name)

    def _collect_requires(self):
        """Collect requires object or dict object."""
        self.requires = [self._parse(os.path.join(self.tempdir, d))
                         for d in os.listdir(self.tempdir)
                         if os.path.isdir(os.path.join(self.tempdir, d))]

    def _parse(self, pkg_dir):
        """Parsing package metadata.

        :rtype: `pkg_resouces.Distributions` or list
        :return: package metadata

        :param str pkg_dir: package directory in build_dir.
        """
        pat = re.compile(r'(\A(.*\.(egg|dist)-info|pip-egg-info)\Z)')
        egg_dirs = [f for f in os.listdir(os.path.join(self.tempdir, pkg_dir))
                    if pat.search(f)]

        if 'pip-egg-info' in egg_dirs:
            egg_info = glob('%s/*' % os.path.join(pkg_dir,
                                                  'pip-egg-info'))[0]
            metadata = self._parse_egg_info(egg_info)
        else:
            dist_info = os.path.join(pkg_dir, egg_dirs[0])
            metadata = self._parse_dist_info(dist_info)
        return metadata

    @staticmethod
    def _parse_egg_info(egg_info):
        """Parse ``.egg-info`` directory.

        :rtype: dict
        :return: dictionary of requires

        :param str egg_info: ``.egg-info`` directory path
        """
        base_dir = os.path.dirname(egg_info)
        metadata = PathMetadata(base_dir, egg_info)
        dist_name = os.path.splitext(os.path.basename(egg_info))[0]
        dist_obj = Distribution(base_dir,
                                project_name=dist_name,
                                metadata=metadata)
        return _dist_to_node(dist_obj)

    @staticmethod
    def _parse_dist_info(dist_info):
        """Parse ``.dist-info`` directory.

        :rtype: dict
        :return: dictionary of requires and test_requires

        :param str dist_info: ``.dist-info`` directory path.
        """
        if os.path.isfile(os.path.join(dist_info, 'metadata.json')):
            with open(os.path.join(dist_info, 'metadata.json'), 'r') as fobj:
                data = fobj.read()
        elif os.path.isfile(os.path.join(dist_info, 'pydist.json')):
            with open(os.path.join(dist_info, 'pydist.json'), 'r') as fobj:
                data = fobj.read()
        metadata = wheel.util.from_json(data)
        if metadata.get('run_requires') is None:
            # To Do: parsing requirements.txt later.
            pass
        return _wheel_to_node(metadata)

    def draw(self, draw_type=None):
        """Generate drawing data.

        :param str draw_type: [dot|blockdiag|linkdraw]
        """
        return graph.router(self.traced_chain, draw_type=draw_type)


def _dist_to_node(dist_obj):
    """Convert distribution metadata to Node objects."""
    node = Node(dist_obj.project_name, version=dist_obj.version)
    node.add_targets([Target(req.project_name, req.specs)
                      for req in dist_obj.requires()])
    return node


def _wheel_to_node(metadata):
    """Convert wheel metadata to Node objects."""
    if metadata.get('extensions'):
        url = (metadata.get('extensions')
               .get('python.details')
               .get('project_urls')
               .get('Home'))
    elif metadata.get('project_urls'):
        url = metadata.get('project_urls').get('Home')
    node = Node(metadata.get('name'),
                version=metadata.get('version'),
                url=url)
    if metadata.get('run_requires'):
        for requires in metadata.get('run_requires'):
            node.add_targets(_parse_require(requires.get('requires')))
    if metadata.get('test_requires'):
        for requires in metadata.get('test_requires'):
            node.add_targets(
                _parse_require(requires.get('requires'), extras=True))
    return node


def _parse_require(requires, extras=False):
    """parse require metadata."""
    targets = []
    for req in requires:
        if len(req.split()) == 1:
            targets.append(Target(req, None, extras))
        else:
            targets.append(Target(req.split()[0], req.split()[1], extras))
    return targets


def u2h(name):
    """Change underscore to hyphen of package name.

    :rtype: str
    :return: string replaced underscore with hyphen

    :param str name: package name
    """
    return name.replace('_', '-')


class Node(object):

    """Node object class."""

    def __init__(self, name, version=None, url=None):
        """Initialize."""
        self.name = name
        self.version = version
        self.url = url
        self.targets = []
        self.test_targets = []

    def __repr__(self):
        """Return Node object name."""
        return str(self.name)

    def add_targets(self, nodes):
        """Add targets."""
        self.targets += nodes

    def remove_targets(self, *nodes):
        """Remove targets."""
        for node in nodes:
            del self.targets[self.targets.index(node)]

    def add_test_targets(self, nodes):
        """Add test targets."""
        self.test_targets += nodes


class Target(Node):

    """Target objects."""

    def __init__(self, nodename, specs, extras=False):
        """Initialize."""
        super(Target, self).__init__(nodename)
        #: specs
        self.specs = specs
        #: extras: True is extras when test_requries (False in default)
        self.extras = extras
