# -*- coding: utf-8 -*-
"""py_deps.tests.test_deps module."""
import sys
import unittest
import os
import tempfile
import shutil
import json
from glob import glob
from mock import patch
from py_deps import deps


@patch('pip.req.RequirementSet.prepare_files')
def prepare(pkg_name, meta_type, cache, _mock):
    """Prepare package object."""
    pkg = deps.Package(pkg_name)
    for meta in glob('py_deps/tests/data/meta/%s/*' % meta_type):
        shutil.copytree(meta,
                        os.path.join(pkg.tempdir,
                                     os.path.basename(meta)))
    pkg.trace_chain()
    cache.store_data(pkg_name, pkg.traced_chain)
    return pkg


def search_result():
    """generate dummy result."""
    with open('py_deps/tests/data/search_result') as fobj:
        return json.loads(fobj.read())


class SearchTests(unittest.TestCase):

    """Test of search via XMLRPC."""

    if sys.version_info < (3, 0):
        @patch('xmlrpclib.ServerProxy')
        def test_search(self, _mock):
            """search package."""
            client_mock = _mock.return_value
            client_mock.search.return_value = search_result()
            self.assertListEqual(deps.Package.search('deps'), search_result())

        @patch('xmlrpclib.ServerProxy')
        def test_search_exactly(self, _mock):
            """search package exactly."""
            client_mock = _mock.return_value
            client_mock.search.return_value = search_result()
            self.assertListEqual(deps.Package.search('py-deps', exactly=True),
                                 [search_result()[8]])

    if sys.version_info > (3, 0):
        @patch('xmlrpc.client.ServerProxy')
        def test_search_py3(self, _mock):
            """search package."""
            client_mock = _mock.return_value
            client_mock.search.return_value = search_result()
            self.assertListEqual(deps.Package.search('deps'), search_result())

        @patch('xmlrpc.client.ServerProxy')
        def test_search_exactly_py3(self, _mock):
            """search package exactly."""
            client_mock = _mock.return_value
            client_mock.search.return_value = search_result()
            self.assertListEqual(deps.Package.search('py-deps', exactly=True),
                                 [search_result()[8]])


class WheelTests(unittest.TestCase):

    """Test of Package class."""

    cache = 'py-deps.tests'

    def setUp(self):
        """Initialize."""
        # self.maxDiff = None
        with open('py_deps/tests/data/wheel.pretty_print') as fobj:
            self.pretty_print = fobj.read()

        with open('py_deps/tests/data/wheel.linkdraw') as fobj:
            self.linkdraw = json.loads(fobj.read())

        deps.DEFAULT_CACHE_NAME = self.cache
        self.container = deps.Container(self.cache)
        self.pkg = prepare('py-deps', 'wheel', self.container)
        self.tempdir = tempfile.mkdtemp(suffix=deps.SUFFIX)

    def tearDown(self):
        """Clean up test."""
        self.pkg.cleanup()
        os.remove(deps.DEFAULT_CACHE_NAME)

    def test_pretty_print(self):
        """Pretty print test."""
        self.assertEqual(self.pkg.draw(),
                         self.pretty_print)

        # cache test
        pkg_cache = deps.Package('py-deps',
                                 cache_name=self.cache)
        self.assertEqual(pkg_cache.draw(),
                         self.pretty_print)
        self.assertEqual(len(self.container.list_data().get('py-deps')), 4)

    def test_linkdraw(self):
        """Linkdraw test."""
        data = json.loads(self.pkg.draw('linkdraw'))
        data['time'] = None
        self.linkdraw['time'] = None
        self.assertEqual(data, self.linkdraw)

    def test_networkx(self):
        """Networkx test."""
        self.assertEqual(len(self.pkg.draw('networkx').nodes()), 20)
        self.assertEqual(len(self.pkg.draw('networkx').edges()), 21)

    def test_cleanup_all(self):
        """Cleanup tests."""
        self.pkg.cleanup(alldir=True)
        self.assertListEqual(
            glob('%s/tmp*%s' % (os.path.dirname(self.tempdir), deps.SUFFIX)),
            [])


class WheelDeprecatedTests(unittest.TestCase):

    """Test of Package class for old style wheel."""

    cache = 'py-deps.tests'

    def setUp(self):
        """Initialize."""
        # self.maxDiff = None
        with open('py_deps/tests/data/wheel-deprecated.pretty_print') as fobj:
            self.pretty_print = fobj.read()

        with open('py_deps/tests/data/wheel-deprecated.linkdraw') as fobj:
            self.linkdraw = json.loads(fobj.read())

        deps.DEFAULT_CACHE_NAME = self.cache
        self.container = deps.Container(self.cache)
        self.pkg = prepare('iso8601', 'wheel-deprecated', self.container)
        self.tempdir = tempfile.mkdtemp(suffix=deps.SUFFIX)

    def tearDown(self):
        """Clean up test."""
        self.pkg.cleanup()
        os.remove(deps.DEFAULT_CACHE_NAME)

    def test_pretty_print(self):
        """Pretty print test."""
        self.assertEqual(self.pkg.draw(),
                         self.pretty_print)

        # cache test
        pkg_cache = deps.Package('iso8601',
                                 cache_name=self.cache)
        self.assertEqual(pkg_cache.draw(),
                         self.pretty_print)
        self.assertEqual(len(self.container.list_data().get('iso8601')), 1)

    def test_linkdraw(self):
        """Linkdraw test."""
        data = json.loads(self.pkg.draw('linkdraw'))
        data['time'] = None
        self.linkdraw['time'] = None
        self.assertEqual(data, self.linkdraw)

    def test_networkx(self):
        """Networkx test."""
        self.assertEqual(len(self.pkg.draw('networkx').nodes()), 1)
        self.assertEqual(len(self.pkg.draw('networkx').edges()), 0)

    def test_cleanup_all(self):
        """Cleanup tests."""
        self.pkg.cleanup(alldir=True)
        self.assertListEqual(
            glob('%s/tmp*%s' % (os.path.dirname(self.tempdir), deps.SUFFIX)),
            [])


class EggTests(unittest.TestCase):

    """Test of Package class."""

    cache = 'py-deps.tests'

    def setUp(self):
        """Initialize."""
        # self.maxDiff = None
        with open('py_deps/tests/data/egg.pretty_print') as fobj:
            self.pretty_print = fobj.read()

        with open('py_deps/tests/data/egg.linkdraw') as fobj:
            self.linkdraw = json.loads(fobj.read())

        deps.DEFAULT_CACHE_NAME = self.cache
        self.container = deps.Container(self.cache)
        self.pkg = prepare('swiftsc', 'egg', self.container)
        self.tempdir = tempfile.mkdtemp(suffix=deps.SUFFIX)

    def tearDown(self):
        """Clean up test."""
        self.pkg.cleanup()
        os.remove(deps.DEFAULT_CACHE_NAME)

    def test_pretty_print(self):
        """Pretty print test."""
        self.assertEqual(self.pkg.draw(),
                         self.pretty_print)

        # cache test
        pkg_cache = deps.Package('swiftsc',
                                 cache_name=self.cache)
        self.assertEqual(pkg_cache.draw(),
                         self.pretty_print)
        self.assertEqual(len(self.container.list_data().get('swiftsc')), 4)

    def test_linkdraw(self):
        """Linkdraw test."""
        data = json.loads(self.pkg.draw('linkdraw'))
        data['time'] = None
        self.linkdraw['time'] = None
        self.assertEqual(data, self.linkdraw)

    def test_networkx(self):
        """Networkx test."""
        self.assertEqual(len(self.pkg.draw('networkx').nodes()), 11)
        self.assertEqual(len(self.pkg.draw('networkx').edges()), 10)

    def test_cleanup_all(self):
        """Cleanup tests."""
        self.pkg.cleanup(alldir=True)
        self.assertListEqual(
            glob('%s/tmp*%s' % (os.path.dirname(self.tempdir), deps.SUFFIX)),
            [])
