# -*- coding: utf-8 -*-
"""py_deps.graph module."""
import networkx
from datetime import datetime


def router(package, draw_type=None, link_prefix=None):
    """Routing drawing tool."""
    if draw_type == 'networkx':
        nwx = Networkx(package, link_prefix)
        return nwx.generate_data()
    if draw_type == 'blockdiag':
        pass
    elif draw_type == 'linkdraw':
        linkdraw = Linkdraw(package, link_prefix)
        draw_data = linkdraw.generate_data()
    else:
        draw_data = '\n'.join(pretty_print(package.traced_chain))
    return draw_data


def edge_key(source_node, target_node):
    """Edge source_node -> target_node key."""
    return f'{source_node.name}=>{target_node.name}'


def generate_data(chain_data, func):
    """Generate dependencies graph."""
    lines = list()
    for node in chain_data:
        if len(node.targets) > 0:
            lines.append(func(node))
            lines += generate_data(node.targets, func)
    return lines


def pretty_print(chain_data):
    """Pretty print on terminal.

    :param list chain_data: List of `deps.Node`
    """
    def node_edge(node):
        return f'{node} -> {node.targets}'
    return generate_data(chain_data, func=node_edge)


class Graph:
    """Graph data generate abstract class."""

    default_radius = "6"
    default_color = "#ff9900"
    requires_color = "#5F9EA0"
    default_width = "1"

    def __init__(self, package, link_prefix=None):
        """Initialize."""
        self.package = package
        self.chain_data = package.traced_chain
        self.link_prefix = link_prefix
        self.check_set = set()

    def __generate_node_dict(self, node):
        return dict(name=self._normalize_name(node.name),
                    r=self.default_radius,
                    color=color(node.depth),
                    version=node.version,
                    link=self._normalize_url(
                        node.url,
                        self._normalize_name(node.name),
                        node.version),
                    depth=node.depth)

    def _generate_nodes(self, chain_data):
        """Generate nodes data."""
        nodes = []
        for node in chain_data:
            if node.name not in self.check_set:
                nodes.append(self.__generate_node_dict(node))
                self.check_set.add(node.name)
                if len(node.targets) > 0:
                    nodes += self._generate_nodes(node.targets)
        return nodes

    def _normalize_url(self, url, node_name, version):
        """Return package url."""
        if self.link_prefix:
            if version:
                normalize_url = f'{self.link_prefix}/{node_name}/{version}'
            else:
                normalize_url = f'{self.link_prefix}/{node_name}'
        elif url:
            normalize_url = url
        else:
            normalize_url = ''
        return normalize_url

    @staticmethod
    def _normalize_name(name):
        """Normalize name."""
        return name


class Linkdraw(Graph):
    """Linkdraw object class."""

    edge_descr = '->'

    def __init__(self, package, link_prefix=None):
        """Initialize."""
        super().__init__(package, link_prefix=link_prefix)
        self.descr = f'{self.package.name} dependencies'
        self.time = datetime.utcnow().isoformat()

    def __generate_edge_dict(self, source_node, target_node):
        return dict(source=self._normalize_name(source_node.name),
                    target=self._normalize_name(target_node.name),
                    color=color(source_node.depth),
                    width=self.default_width,
                    descr=self.edge_descr,
                    link='')

    def __generate_edges(self, source_node, target_nodes):
        """Generate edges data."""
        edges = []
        for target_node in target_nodes:
            _edge_key = edge_key(source_node, target_node)
            if _edge_key not in self.check_set:
                edge = self.__generate_edge_dict(source_node, target_node)
                if edge not in edges:
                    edges.append(edge)
                    self.check_set.add(_edge_key)
                if len(target_node.targets) > 0:
                    edges += self.__generate_edges(target_node,
                                                   target_node.targets)
        return edges

    def generate_data(self):
        """Generate Linkdraw data."""
        nodes = self._generate_nodes(self.chain_data)
        self.check_set.clear()
        lines = self.__generate_edges(self.chain_data[0],
                                      self.chain_data[0].targets)
        self.check_set.clear()
        return dict(time=self.time,
                    descr=self.descr,
                    nodes=nodes,
                    lines=lines)

    @staticmethod
    def _normalize_name(name):
        """Normalize name."""
        return name.replace('[', '____').replace(']', '')


class Networkx(Graph):
    """Networkx object class."""

    def __init__(self, package, link_prefix=None):
        """Initialize."""
        super().__init__(package, link_prefix=link_prefix)
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
        for node in self._generate_nodes(self.chain_data):
            self.graph.add_node(node['name'],
                                version=node['version'],
                                link=self._normalize_url(node['link'],
                                                         node['name'],
                                                         node['version']),
                                depth=node['depth'])
        self.generate_edges()
        return self.graph


def color(depth):
    """Color by depth level.

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
