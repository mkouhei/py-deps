# -*- coding: utf-8 -*-
"""py_deps.tests.test_deps module."""
import unittest
from py_deps import deps, graph


class GraphFunctionTests(unittest.TestCase):

    """Tests of graph functions."""

    def setUp(self):
        self.pkg = deps.Package('backup2swift',
                                cache_name='py_deps/tests/data/py-deps.pickle')

    def test_router_pretty_print(self):
        """Test router without draw_type."""
        self.assertTrue(graph.router(self.pkg).startswith('backup2swift -> ['))

    def test_router_linkdraw(self):
        """Test router with draw_type=linkdraw."""
        self.assertEqual(
            graph.router(self.pkg, draw_type='linkdraw').get('descr'),
            f'{self.pkg.name} dependencies'
        )
        self.assertEqual(
            len(graph.router(self.pkg, draw_type='linkdraw').get('nodes')),
            9
        )
        self.assertEqual(
            len(graph.router(self.pkg, draw_type='linkdraw').get('lines')),
            9
        )

    def test_router_networkx(self):
        """Test router with draw_type=networkx."""
        self.assertEqual(
            graph.router(self.pkg, draw_type='networkx').number_of_nodes(),
            9
        )
        self.assertEqual(
            graph.router(self.pkg, draw_type='networkx').number_of_edges(),
            2
        )
