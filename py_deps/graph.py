# -*- coding: utf-8 -*-
"""py_deps.graph module."""
import json
import networkx
from datetime import datetime
from py_deps.exceptions import InvalidMetadata


# pylint: disable=too-many-arguments
def router(chain_data, draw_type=None, decode_type='',
           disable_time=False, disable_descr=False, link_prefix=None):
    """Routing drawing tool."""
    if draw_type == 'networkx':
        nwx = Networkx(chain_data, link_prefix)
        return nwx.generate_data()
    elif draw_type == 'blockdiag':
        pass
    elif draw_type == 'linkdraw':
        linkdraw = Linkdraw(chain_data, link_prefix)
        if disable_time:
            linkdraw.disable_time()
        if disable_descr:
            linkdraw.disable_descr()
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
        lines += '{0} -> {1}\n'.format(node, node.targets)
    return lines.rstrip()


class Graph(object):

    """Graph data generate abstract class."""

    default_radius = "6"
    default_color = "#ff9900"
    requires_color = "#5F9EA0"
    default_width = "1"

    def __init__(self, chain_data, link_prefix=None):
        """Initialize."""
        self.chain_data = chain_data
        self.link_prefix = link_prefix

    def _generate_node(self, node, nodes):
        """Generate node data."""
        if self._check_node(node, nodes):
            metadata = self._get_metadata(node.name)
            nodes.append(dict(name=self._normalize_name(node.name),
                              r=self.default_radius,
                              color=self.default_color,
                              version=metadata.version,
                              link=self._normalize_url(
                                  metadata.url,
                                  self._normalize_name(node.name),
                                  metadata.version),
                              depth=node.depth))
        if node.targets:
            for target in node.targets:
                if self._check_node(target, nodes):
                    metadata = self._get_metadata(target.name)
                    nodes.append(dict(name=self._normalize_name(target.name),
                                      r=self.default_radius,
                                      color=color(target.depth),
                                      version=metadata.version,
                                      link=self._normalize_url(
                                          metadata.url,
                                          self._normalize_name(target.name),
                                          metadata.version),
                                      depth=target.depth))

    def _check_node(self, node, nodes):
        """Check appended node."""
        if ([_node for _node in nodes
             if _node['name'] == self._normalize_name(node.name)]):
            return False
        else:
            return True

    def generate_nodes(self):
        """Generate nodes data."""
        nodes = []
        for node in self.chain_data:
            self._generate_node(node, nodes)
        return nodes

    def _normalize_url(self, url, node_name, version):
        """return package url."""
        if self.link_prefix:
            if version:
                return '{0}/{1}/{2}'.format(self.link_prefix,
                                            node_name,
                                            version)
            else:
                return '{0}/{1}'.format(self.link_prefix, node_name)
        elif url:
            return url
        else:
            return ''

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

    def count_depth(self):
        """Count each depth."""
        nodes = self.generate_nodes()
        return {i: [node.get('depth') for node in nodes].count(i)
                for i in set([node.get('depth') for node in nodes])}


class Metadata(object):

    """Metadata object class."""

    version = None
    url = None


class Linkdraw(Graph):

    """Linkdraw object class."""

    def __init__(self, chain_data, link_prefix=None):
        """Initialize."""
        super(Linkdraw, self).__init__(chain_data, link_prefix=link_prefix)
        try:
            self.descr = "{0} dependencies".format(chain_data[0].name)
        except IndexError:
            raise InvalidMetadata("Package broken.")
        self.time = datetime.utcnow().isoformat()

    def generate_edges(self):
        """Generate edges data."""
        edges = []
        for node in self.chain_data:
            for target in node.targets:
                edge = dict(source=self._normalize_name(node.name),
                            target=self._normalize_name(target.name),
                            color=color(node.depth),
                            width=self.default_width,
                            descr="->",
                            link="")
                if edge not in edges:
                    edges.append(edge)
        return edges

    def generate_data(self):
        """Generate Linkdraw data."""
        return dict(time=self.time,
                    descr=self.descr,
                    nodes=self.generate_nodes(),
                    lines=self.generate_edges())

    @staticmethod
    def _normalize_name(name):
        """Normalize name."""
        return name.replace('[', '____').replace(']', '')

    def disable_descr(self):
        """Disable description."""
        self.descr = None

    def disable_time(self):
        """Disable time."""
        self.time = None

    def generate_position(self):
        """Generate position.

        level 0 is the base depth, that is one only.

        Nodes depth images is follows.::

            0---1---2---3
            |    `--2---3---4---5
            |     `-2---3
            |        `--3---4
            1---2---3
                 `--3

        base position:  0
        level distance: the value that the smaller of the SVG width and height
                        devided by the ``depth level``.
        node disstance: the circumference drawed by the same level nodes
                        devided by the ``num same level``.
        depth level:    len(self.count_depth().key())
        deepest level:  self.count_depth().keys()[-1]
        num same level: self.count_depth().get(int:'some level')
        """
        pass


class Networkx(Graph):

    """Networkx object class."""

    def __init__(self, chain_data, link_prefix=None):
        """Initialize."""
        super(Networkx, self).__init__(chain_data, link_prefix=link_prefix)
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
                                link=self._normalize_url(node['link'],
                                                         node['name'],
                                                         node['version']),
                                depth=node['depth'])
        self.generate_edges()
        return self.graph


def color(depth):
    """color by depth level.

    :rtype: str
    :return: hex color code based blue.
    :param int depth: dependency level
    """
    color_table = ['#d1e0fa',
                   '#a4c1f4',
                   '#76a1ef',
                   '#4882ea',
                   '#1b63e4',
                   '#154fb7',
                   '#103b89',
                   '#0b285b',
                   '#05142e']
    if depth >= len(color_table):
        depth = len(color_table) - 1
    return color_table[depth]
