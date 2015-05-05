# -*- coding: utf-8 -*-
"""py_deps.graph module."""
import json
from datetime import datetime


def router(chain_data, draw_type=None):
    """Routing drawing tool."""
    if draw_type == 'dot':
        pass
    elif draw_type == 'blockdiag':
        pass
    elif draw_type == 'linkdraw':
        linkdraw = Linkdraw(chain_data)
        return linkdraw.generate_data()
    else:
        return pretty_print(chain_data)


def pretty_print(chain_data):
    """Pretty print on terminal.

    :param list chain_data: List of `deps.Node`
    """
    lines = ''
    for node in chain_data:
        lines += '%s -> %s\n' % (node, node.targets)
    return lines.rstrip()


class Linkdraw(object):

    """Linkdraw data generate class."""

    default_radius = "6"
    default_color = ""
    requires_color = "#5F9EA0"
    default_width = "1"

    def __init__(self, chain_data):
        """Initialize."""
        self.chain_data = chain_data
        self.descr = "%s dependencies" % chain_data[0].name

    def _geneate_node(self, node, nodes):
        """Generate node data."""
        if self._check_node(node, nodes):
            nodes.append(dict(name=self._normalize_name(node.name),
                              r=self.default_radius,
                              color=self.default_color,
                              link=self._normalize_url(node.url)))
        if len(node.targets) > 0:
            for target in node.targets:
                if self._check_node(target, nodes):
                    nodes.append(dict(name=self._normalize_name(target.name),
                                      r=self.default_radius,
                                      color=self.requires_color,
                                      link=self._normalize_url(target.url)))

    def _check_node(self, node, nodes):
        """Check appended node."""
        if len([_node for _node in nodes
                if _node['name'] == self._normalize_name(node.name)]) == 0:
            return True
        else:
            return False

    def generate_nodes(self):
        """Generate nodes data."""
        nodes = []
        for node in self.chain_data:
            self._geneate_node(node, nodes)
        return nodes

    def generate_lines(self):
        """Generate lines data."""
        return [dict(source=self._normalize_name(node.name),
                     target=self._normalize_name(target.name),
                     color=self.requires_color,
                     width=self.default_width,
                     descr="→",
                     link="")
                for node in self.chain_data
                for target in node.targets]

    def generate_data(self):
        """Generate Linkdraw data."""
        return json.dumps(dict(time=datetime.utcnow().isoformat(),
                               descr=self.descr,
                               nodes=self.generate_nodes(),
                               lines=self.generate_lines()))

    @staticmethod
    def _normalize_url(url):
        """return package url."""
        if url is None:
            return ''
        else:
            return url

    @staticmethod
    def _normalize_name(name):
        """Normalize name."""
        return name.replace('[', '____').replace(']', '')
