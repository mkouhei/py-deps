# -*- coding: utf-8 -*-
"""py_deps.tests.test_deps module."""

import unittest
import os
import tempfile
import json
from glob import glob
from py_deps import deps


class PackageTests(unittest.TestCase):

    """Test of Package class."""

    cache = 'py-deps.tests'

    def setUp(self):
        """Initialize."""
        # self.maxDiff = None
        with open('py_deps/tests/data/pretty_print') as fobj:
            self.pretty_print = fobj.read()

        with open('py_deps/tests/data/linkdraw') as fobj:
            self.linkdraw = json.loads(fobj.read())

        deps.DEFAULT_CACHE_NAME = self.cache
        self.pkg = deps.Package('py-deps')

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
        self.assertEqual(len(self.pkg.draw('dot').nodes()), 20)
        self.assertEqual(len(self.pkg.draw('dot').edges()), 21)

    def test_cleanup_all(self):
        """Cleanup tests."""
        self.pkg.cleanup(alldir=True)
        self.assertListEqual(
            glob('%s/tmp*%s' % (os.path.dirname(self.tempdir), deps.SUFFIX)),
            [])
