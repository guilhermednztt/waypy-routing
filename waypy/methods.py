"""Unweighted graph search algorithms."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Hashable, Iterable, Mapping, TypeAlias

from waypy.exceptions import UnknownSearchMethodError
from waypy.graphs import Graph

Node: TypeAlias = Hashable
Path: TypeAlias = list[Node]


class SearchMethod(str, Enum):
    """Supported unweighted search methods."""

    BREADTH_FIRST = "breadth_first"
    DEPTH_FIRST = "depth_first"
    LIMITED_DEPTH = "limited_depth"
    ITERATIVE_DEEPENING = "iterative_deepening"
    BIDIRECTIONAL = "bidirectional"


UNWEIGHTED_METHOD_ALIASES: Mapping[str, SearchMethod] = {
    "BREADTH_FIRST": SearchMethod.BREADTH_FIRST,
    "BFS": SearchMethod.BREADTH_FIRST,
    "AMPLITUDE": SearchMethod.BREADTH_FIRST,
    "DEPTH_FIRST": SearchMethod.DEPTH_FIRST,
    "DFS": SearchMethod.DEPTH_FIRST,
    "PROFUNDIDADE": SearchMethod.DEPTH_FIRST,
    "LIMITED_DEPTH": SearchMethod.LIMITED_DEPTH,
    "PROFUNDIDADE LIMITADA": SearchMethod.LIMITED_DEPTH,
    "ITERATIVE_DEEPENING": SearchMethod.ITERATIVE_DEEPENING,
    "APROFUNDAMENTO ITERATIVO": SearchMethod.ITERATIVE_DEEPENING,
    "BIDIRECTIONAL": SearchMethod.BIDIRECTIONAL,
    "BIDIRECIONAL": SearchMethod.BIDIRECTIONAL,
}


def normalize_search_method(method: str | SearchMethod) -> SearchMethod:
    """Return a normalized unweighted search method."""

    if isinstance(method, SearchMethod):
        return method

    key = method.strip().replace("-", "_").upper()
    try:
        return UNWEIGHTED_METHOD_ALIASES[key]
    except KeyError as exc:
        raise UnknownSearchMethodError(f"Unsupported search method: {method}") from exc


@dataclass(slots=True)
class SearchAlgorithms:
    """Collection of pure unweighted graph search algorithms."""

    @staticmethod
    def breadth_first(graph: Graph, start: Node, goal: Node) -> Path | None:
        if start == goal:
            return [start]
        if start not in graph or goal not in graph:
            return None

        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            current, path = queue.popleft()
            for neighbor in graph[current]:
                if neighbor in visited:
                    continue

                next_path = [*path, neighbor]
                if neighbor == goal:
                    return next_path

                visited.add(neighbor)
                queue.append((neighbor, next_path))

        return None

    @staticmethod
    def depth_first(graph: Graph, start: Node, goal: Node) -> Path | None:
        if start == goal:
            return [start]
        if start not in graph or goal not in graph:
            return None

        stack = [(start, [start])]
        visited = set()

        while stack:
            current, path = stack.pop()
            if current in visited:
                continue

            visited.add(current)
            if current == goal:
                return path

            for neighbor in reversed(graph[current]):
                if neighbor not in visited:
                    stack.append((neighbor, [*path, neighbor]))

        return None

    @staticmethod
    def limited_depth(
        graph: Graph,
        start: Node,
        goal: Node,
        limit: int,
    ) -> Path | None:
        if limit < 0:
            raise ValueError("limit must be greater than or equal to zero")
        if start == goal:
            return [start]
        if start not in graph or goal not in graph:
            return None

        stack = [(start, [start], 0)]

        while stack:
            current, path, depth = stack.pop()
            if current == goal:
                return path
            if depth >= limit:
                continue

            for neighbor in reversed(graph[current]):
                if neighbor not in path:
                    stack.append((neighbor, [*path, neighbor], depth + 1))

        return None

    @staticmethod
    def iterative_deepening(graph: Graph, start: Node, goal: Node) -> Path | None:
        if start == goal:
            return [start]

        max_depth = max(len(graph) - 1, 0)
        for limit in range(max_depth + 1):
            path = SearchAlgorithms.limited_depth(graph, start, goal, limit)
            if path is not None:
                return path

        return None

    @staticmethod
    def bidirectional(graph: Graph, start: Node, goal: Node) -> Path | None:
        if start == goal:
            return [start]
        if start not in graph or goal not in graph:
            return None

        reverse_graph = _reverse_graph(graph)
        forward_queue = deque([start])
        backward_queue = deque([goal])
        forward_parent: dict[Node, Node | None] = {start: None}
        backward_parent: dict[Node, Node | None] = {goal: None}

        while forward_queue and backward_queue:
            meeting = _expand_frontier(graph, forward_queue, forward_parent, backward_parent)
            if meeting is not None:
                return _build_bidirectional_path(meeting, forward_parent, backward_parent)

            meeting = _expand_frontier(
                reverse_graph,
                backward_queue,
                backward_parent,
                forward_parent,
            )
            if meeting is not None:
                return _build_bidirectional_path(meeting, forward_parent, backward_parent)

        return None

    @staticmethod
    def search(
        graph: Graph,
        start: Node,
        goal: Node,
        method: str | SearchMethod = SearchMethod.BREADTH_FIRST,
        limit: int | None = None,
    ) -> Path | None:
        normalized_method = normalize_search_method(method)

        if normalized_method is SearchMethod.BREADTH_FIRST:
            return SearchAlgorithms.breadth_first(graph, start, goal)
        if normalized_method is SearchMethod.DEPTH_FIRST:
            return SearchAlgorithms.depth_first(graph, start, goal)
        if normalized_method is SearchMethod.LIMITED_DEPTH:
            return SearchAlgorithms.limited_depth(graph, start, goal, limit or 0)
        if normalized_method is SearchMethod.ITERATIVE_DEEPENING:
            return SearchAlgorithms.iterative_deepening(graph, start, goal)
        if normalized_method is SearchMethod.BIDIRECTIONAL:
            return SearchAlgorithms.bidirectional(graph, start, goal)

        raise UnknownSearchMethodError(f"Unsupported search method: {method}")


def _expand_frontier(
    graph: Graph,
    queue: deque[Node],
    own_parent: dict[Node, Node | None],
    other_parent: Mapping[Node, Node | None],
) -> Node | None:
    for _ in range(len(queue)):
        current = queue.popleft()
        for neighbor in graph[current]:
            if neighbor in own_parent:
                continue

            own_parent[neighbor] = current
            if neighbor in other_parent:
                return neighbor

            queue.append(neighbor)

    return None


def _build_bidirectional_path(
    meeting: Node,
    forward_parent: Mapping[Node, Node | None],
    backward_parent: Mapping[Node, Node | None],
) -> Path:
    forward_path = _trace_path(meeting, forward_parent)
    backward_path = _trace_path(meeting, backward_parent)
    return [*reversed(forward_path), *backward_path[1:]]


def _trace_path(node: Node, parents: Mapping[Node, Node | None]) -> Path:
    path = [node]
    while parents[node] is not None:
        node = parents[node]
        path.append(node)
    return path


def _reverse_graph(graph: Graph) -> Graph:
    reversed_graph: dict[Node, list[Node]] = {node: [] for node in graph}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            reversed_graph.setdefault(neighbor, []).append(node)
    return reversed_graph


class busca:
    """Backward-compatible wrapper for the original Portuguese API."""

    def amplitude(self, inicio: Node, fim: Node, nos: Iterable[Node], grafo: Iterable[Iterable[Node]]) -> Path | None:
        from waypy.graphs import build_graph

        return SearchAlgorithms.breadth_first(build_graph(nos, grafo), inicio, fim)

    def profundidade(self, inicio: Node, fim: Node, nos: Iterable[Node], grafo: Iterable[Iterable[Node]]) -> Path | None:
        from waypy.graphs import build_graph

        return SearchAlgorithms.depth_first(build_graph(nos, grafo), inicio, fim)

    def profundidade_limitada(
        self,
        inicio: Node,
        fim: Node,
        limite: int,
        nos: Iterable[Node],
        grafo: Iterable[Iterable[Node]],
    ) -> Path | None:
        from waypy.graphs import build_graph

        return SearchAlgorithms.limited_depth(build_graph(nos, grafo), inicio, fim, limite)

    def aprofundamento_iterativo(self, inicio: Node, fim: Node, nos: Iterable[Node], grafo: Iterable[Iterable[Node]]) -> Path | None:
        from waypy.graphs import build_graph

        return SearchAlgorithms.iterative_deepening(build_graph(nos, grafo), inicio, fim)

    def bidirecional(self, inicio: Node, fim: Node, nos: Iterable[Node], grafo: Iterable[Iterable[Node]]) -> Path | None:
        from waypy.graphs import build_graph

        return SearchAlgorithms.bidirectional(build_graph(nos, grafo), inicio, fim)
