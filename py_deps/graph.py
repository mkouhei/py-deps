# -*- coding: utf-8 -*-
"""py_deps.graph module."""


def router(chain_data, draw_type=None):
    """Routing drawing tool."""
    if draw_type == 'dot':
        pass
    elif draw_type == 'blockdiag':
        pass
    elif draw_type == 'linkdraw':
        pass
    else:
        pretty_print(chain_data)


def pretty_print(chain_data):
    """Pretty print on terminal.

    :param list chain_data: List of `deps.Node`
    """
    for node in chain_data:
        print('%s -> %s' % (node, node.targets))
