# -*- coding: utf-8 -*-
"""py_deps.tests.test_deps module."""

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
        cache = deps.Container(self.cache)
        self.pkg = prepare('py-deps', 'wheel', cache)
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
        cache = deps.Container(self.cache)
        self.pkg = prepare('swiftsc', 'egg', cache)
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
