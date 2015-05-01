# -*- coding: utf-8 -*-
"""py_deps.deps module."""
import os
import tempfile
import re
import pip.util
import wheel.util
from glob import glob
from pip.req import RequirementSet, InstallRequirement
from pip.locations import src_prefix
from pip.index import PackageFinder
from pkg_resources import PathMetadata, Distribution


SUFFIX = '-py_deps'


class Package(object):

    """Package class."""

    #: index_url
    index_url = 'https://pypi.python.org/simple'

    def __init__(self, name):
        """Initialize to parsing dependencies of package."""
        self.name = name
        self.tempdir = tempfile.mkdtemp(suffix=SUFFIX)

        self.finder = PackageFinder(find_links=[],
                                    index_urls=[self.index_url])
        self.reqset = RequirementSet(build_dir=self.tempdir,
                                     src_dir=src_prefix,
                                     download_dir=None,
                                     upgrade=True)

        req = InstallRequirement.from_line(name,
                                           comes_from=None)
        self.reqset.add_requirement(req)
        self.requires = []

    def cleanup(self, alldir=False):
        """Cleanup temporary build directory.

        :param bool alldir: Remove all temporary directories. (default: False)

        :rtype: None
        """
        if alldir:
            for tempdir in glob("%s/tmp*%s" % (os.path.dirname(self.tempdir),
                                               SUFFIX)):
                pip.util.rmtree(tempdir, ignore_errors=True)
        else:
            pip.util.rmtree(self.tempdir, ignore_errors=True)

    def _download(self):
        """Download packages to build_dir.

        This method does not download requires recursively.
        """
        self.reqset.prepare_files(self.finder)

    def list_requires(self):
        """Listing requires object or dict object.

        :rtype: list
        :return: requires object or dict object
        """
        if not self.requires:
            self._download()
            self._collect_requires()
            self.cleanup()
        return self.requires

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
        with open('%s/metadata.json' % dist_info, 'r') as fobj:
            data = fobj.read()
        metadata = wheel.util.from_json(data)
        if metadata.get('run_requires') is None:
            # To Do: parsing requirements.txt later.
            pass
        return _wheel_to_node(metadata)


def _dist_to_node(dist_obj):
    """Convert distribution metadata to Node objects."""
    node = Node(dist_obj.project_name, version=dist_obj.version)
    node.add_targets([Target(req.project_name, req.specs)
                      for req in dist_obj.requires()])
    return node


def _wheel_to_node(metadata):
    """Convert wheel metadata to Node objects."""
    node = Node(metadata.get('name'),
                version=metadata.get('version'))
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
