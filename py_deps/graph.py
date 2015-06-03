# -*- coding: utf-8 -*-
"""py_deps.graph module."""
import json
import networkx
from datetime import datetime


def router(chain_data, draw_type=None, decode_type=''):
    """Routing drawing tool."""
    if draw_type == 'networkx':
        nwx = Networkx(chain_data)
        return nwx.generate_data()
    elif draw_type == 'blockdiag':
        pass
    elif draw_type == 'linkdraw':
        linkdraw = Linkdraw(chain_data)
        if decode_type == 'json':
            return linkdraw.generate_data()
        else:
            return json.dumps(linkdraw.generate_data())
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


class Graph(object):

    """Graph data generate abstract class."""

    default_radius = "6"
    default_color = ""
    requires_color = "#5F9EA0"
    default_width = "1"

    def __init__(self, chain_data):
        """Initialize."""
        self.chain_data = chain_data

    def _generate_node(self, node, nodes):
        """Generate node data."""
        if self._check_node(node, nodes):
            metadata = self._get_metadata(node.name)
            nodes.append(dict(name=self._normalize_name(node.name),
                              r=self.default_radius,
                              color=self.default_color,
                              version=metadata.version,
                              link=self._normalize_url(metadata.url)))
        if len(node.targets) > 0:
            for target in node.targets:
                if self._check_node(target, nodes):
                    metadata = self._get_metadata(target.name)
                    nodes.append(dict(name=self._normalize_name(target.name),
                                      r=self.default_radius,
                                      color=self.requires_color,
                                      version=metadata.version,
                                      link=self._normalize_url(metadata.url)))

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
            self._generate_node(node, nodes)
        return nodes

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
        return name

    def _get_metadata(self, name):
        """get the metadata of package."""
        data = [req for req in self.chain_data if req.name == name]
        if len(data) == 1:
            return data[0]
        else:
            return Metadata()


class Metadata(object):

    """Metadata object class."""

    version = None
    url = None


class Linkdraw(Graph):

    """Linkdraw object class."""

    def __init__(self, chain_data):
        """Initialize."""
        super(Linkdraw, self).__init__(chain_data)
        self.descr = "%s dependencies" % chain_data[0].name

    def generate_edges(self):
        """Generate edges data."""
        return [dict(source=self._normalize_name(node.name),
                     target=self._normalize_name(target.name),
                     color=self.requires_color,
                     width=self.default_width,
                     descr="->",
                     link="")
                for node in self.chain_data
                for target in node.targets]

    def generate_data(self):
        """Generate Linkdraw data."""
        return dict(time=datetime.utcnow().isoformat(),
                    descr=self.descr,
                    nodes=self.generate_nodes(),
                    lines=self.generate_edges())

    @staticmethod
    def _normalize_name(name):
        """Normalize name."""
        return name.replace('[', '____').replace(']', '')


class Networkx(Graph):

    """Networkx object class."""

    def __init__(self, chain_data):
        """Initialize."""
        super(Networkx, self).__init__(chain_data)
        self.graph = networkx.DiGraph()

    def generate_edges(self):
        """Generate edges data."""
        self.graph.add_edges_from([(self._normalize_name(node.name),
                                    self._normalize_name(target.name))
                                   for node in self.chain_data
                                   for target in node.targets],
                                  color=self.requires_color)

    def generate_data(self):
        """Generate networkx graph data."""
        for node in self.generate_nodes():
            self.graph.add_node(node['name'],
                                version=node['version'],
                                link=node['link'])
        self.generate_edges()
        return self.graph
