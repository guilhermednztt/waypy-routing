"""Graph conversion and validation helpers."""

from __future__ import annotations

from typing import Hashable, Iterable, Mapping, Sequence, TypeAlias

from waypy.exceptions import InvalidGraphError

Node: TypeAlias = Hashable
Graph: TypeAlias = dict[Node, list[Node]]
WeightedEdge: TypeAlias = tuple[Node, float]
WeightedGraph: TypeAlias = dict[Node, list[WeightedEdge]]


def build_graph(nodes: Iterable[Node], edges: Iterable[Iterable[Node]]) -> Graph:
    """Build an adjacency-list graph from parallel node and edge collections."""

    node_list = list(nodes)
    edge_list = [list(neighbors) for neighbors in edges]
    _validate_parallel_lengths(node_list, edge_list)

    graph: Graph = {node: [] for node in node_list}
    known_nodes = set(node_list)

    for node, neighbors in zip(node_list, edge_list):
        for neighbor in neighbors:
            if neighbor not in known_nodes:
                raise InvalidGraphError(f"Unknown neighbor {neighbor!r} referenced by {node!r}")
            graph[node].append(neighbor)

    return graph


def build_weighted_graph(
    nodes: Iterable[Node],
    edges: Iterable[Iterable[Sequence[object]]],
) -> WeightedGraph:
    """Build a weighted adjacency-list graph from parallel node and edge collections."""

    node_list = list(nodes)
    edge_list = [list(neighbors) for neighbors in edges]
    _validate_parallel_lengths(node_list, edge_list)

    graph: WeightedGraph = {node: [] for node in node_list}
    known_nodes = set(node_list)

    for node, neighbors in zip(node_list, edge_list):
        for edge in neighbors:
            if len(edge) != 2:
                raise InvalidGraphError("Weighted edges must contain a target node and a numeric cost")

            neighbor = edge[0]
            cost = edge[1]
            if neighbor not in known_nodes:
                raise InvalidGraphError(f"Unknown neighbor {neighbor!r} referenced by {node!r}")
            if not isinstance(cost, int | float):
                raise InvalidGraphError(f"Edge cost for {node!r} -> {neighbor!r} must be numeric")
            if cost < 0:
                raise InvalidGraphError("Weighted search does not support negative edge costs")

            graph[node].append((neighbor, float(cost)))

    return graph


def ensure_graph(graph: Mapping[Node, Iterable[Node]] | Graph) -> Graph:
    """Return a defensive copy of an adjacency-list graph."""

    copied = {node: list(neighbors) for node, neighbors in graph.items()}
    known_nodes = set(copied)
    for node, neighbors in copied.items():
        for neighbor in neighbors:
            if neighbor not in known_nodes:
                raise InvalidGraphError(f"Unknown neighbor {neighbor!r} referenced by {node!r}")
    return copied


def ensure_weighted_graph(
    graph: Mapping[Node, Iterable[Sequence[object] | WeightedEdge]] | WeightedGraph,
) -> WeightedGraph:
    """Return a defensive copy of a weighted adjacency-list graph."""

    copied: WeightedGraph = {}
    known_nodes = set(graph)

    for node, edges in graph.items():
        copied[node] = []
        for edge in edges:
            if len(edge) != 2:
                raise InvalidGraphError("Weighted edges must contain a target node and a numeric cost")

            neighbor = edge[0]
            cost = edge[1]
            if neighbor not in known_nodes:
                raise InvalidGraphError(f"Unknown neighbor {neighbor!r} referenced by {node!r}")
            if not isinstance(cost, int | float):
                raise InvalidGraphError(f"Edge cost for {node!r} -> {neighbor!r} must be numeric")
            if cost < 0:
                raise InvalidGraphError("Weighted search does not support negative edge costs")

            copied[node].append((neighbor, float(cost)))

    return copied


def _validate_parallel_lengths(nodes: list[Node], edges: list[object]) -> None:
    if len(nodes) != len(edges):
        raise InvalidGraphError("nodes and edges must have the same length")
    if len(set(nodes)) != len(nodes):
        raise InvalidGraphError("nodes must not contain duplicates")
