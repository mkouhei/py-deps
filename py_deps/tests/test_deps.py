# -*- coding: utf-8 -*-
"""py_deps.tests.test_deps module."""
import unittest
import itertools
import os
from mock import patch
from py_deps import deps
from py_deps.exceptions import BackendFailure


class SearchTests(unittest.TestCase):

    """Test of search via XMLRPC."""

    def setUp(self):
        self.search_result = [
            {'name': 'py-deps',
             'summary': 'parsing the Python deps and generating graph data',
             'version': '0.5.5',
             '_pypi_ordering': False},
            {'name': 'deps',
             'summary': 'deps discovers your Python dependencies',
             'version': '0.1.0',
             '_pypi_ordering': False},
            {'name': 'mysqlclient-deps',
             'summary': '',
             'version': '0.0.2',
             '_pypi_ordering': False}]

    @patch('xmlrpc.client.ServerProxy')
    def test_search(self, _mock):
        """search package."""
        client_mock = _mock.return_value
        client_mock.search.return_value = self.search_result
        self.assertListEqual(deps.search('deps'), self.search_result)

    @patch('xmlrpc.client.ServerProxy')
    def test_search_raise_error(self, _mock):
        """search package."""
        client_mock = _mock.return_value
        client_mock.search.side_effect = TimeoutError
        with self.assertRaises(BackendFailure):
            deps.search('deps')

    @patch('xmlrpc.client.ServerProxy')
    def test_search_exactly(self, _mock):
        """search package exactly."""
        client_mock = _mock.return_value
        client_mock.search.return_value = self.search_result
        self.assertListEqual(deps.search('py-deps', exactly=True),
                             [self.search_result[0]])

    @patch('xmlrpc.client.ServerProxy')
    def test_latest_version(self, _mock):
        """search latest version."""
        client_mock = _mock.return_value
        version = self.search_result[0].get('version')
        client_mock.package_releases.return_value = [version]
        self.assertEqual(deps.latest_version('py-deps'), version)

    @patch('xmlrpc.client.ServerProxy')
    def test_latest_version_not_responses(self, _mock):
        """search latest version."""
        client_mock = _mock.return_value
        client_mock.package_releases.return_value = []
        self.assertEqual(deps.latest_version('py-deps'), '')

    @patch('xmlrpc.client.ServerProxy')
    def test_latest_version_raise_error(self, _mock):
        """search latest version."""
        client_mock = _mock.return_value
        client_mock.package_releases.side_effect = TimeoutError
        with self.assertRaises(BackendFailure):
            deps.latest_version('py-deps')

    def test_u2h(self):
        """teest convert underscore to hyphen."""
        self.assertEqual(deps.u2h('foo_bar'), 'foo-bar')


class PackageTests(unittest.TestCase):

    """Test of Package class."""

    def setUp(self):
        self.pkg = deps.Package('backup2swift',
                                cache_name='py_deps/tests/data/py-deps.pickle')

    def test_constructor(self):
        """Test contstructor."""
        self.assertEqual(self.pkg.name, 'backup2swift')
        self.assertIsNone(self.pkg.version)
        self.assertFalse(os.path.isdir(self.pkg.tempdir))
        self.assertEqual(len(self.pkg.traced_chain), 1)
        self.assertEqual(self.pkg.traced_chain[0].name, 'backup2swift')
        self.assertEqual(len(self.pkg.traced_chain[0].targets), 2)
        flatten_list = itertools.chain.from_iterable(
            [i.targets for i in self.pkg.traced_chain[0].targets]
        )
        self.assertEqual(len(list(flatten_list)), 3)

    def test_draw(self):
        """Test draw method."""
        self.assertEqual(
            len(
                self.pkg.draw(
                    draw_type='linkdraw', link_prefix='/graph'
                ).get('nodes')
            ), 9)
