"""Weighted graph search algorithms."""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from enum import Enum
from itertools import count
from typing import Hashable, Mapping, TypeAlias

from waypy.exceptions import UnknownSearchMethodError
from waypy.graphs import WeightedGraph

Node: TypeAlias = Hashable
Path: TypeAlias = list[Node]
Heuristic: TypeAlias = Mapping[Node, float] | Mapping[Node, Mapping[Node, float]]


class WeightedSearchMethod(str, Enum):
    """Supported weighted search methods."""

    A_STAR = "a_star"
    GREEDY = "greedy"
    UNIFORM_COST = "uniform_cost"


WEIGHTED_METHOD_ALIASES: Mapping[str, WeightedSearchMethod] = {
    "A_STAR": WeightedSearchMethod.A_STAR,
    "A_ESTRELA": WeightedSearchMethod.A_STAR,
    "GREEDY": WeightedSearchMethod.GREEDY,
    "UNIFORM_COST": WeightedSearchMethod.UNIFORM_COST,
    "CUSTO_UNIFORME": WeightedSearchMethod.UNIFORM_COST,
}


def normalize_weighted_search_method(method: str | WeightedSearchMethod) -> WeightedSearchMethod:
    """Return a normalized weighted search method."""

    if isinstance(method, WeightedSearchMethod):
        return method

    key = method.strip().replace("-", "_").upper()
    try:
        return WEIGHTED_METHOD_ALIASES[key]
    except KeyError as exc:
        raise UnknownSearchMethodError(f"Unsupported weighted search method: {method}") from exc


@dataclass(slots=True)
class WeightedSearchResult:
    """Path and total cost returned by weighted search algorithms."""

    path: Path
    cost: float


@dataclass(slots=True)
class WeightedSearchAlgorithms:
    """Collection of pure weighted graph search algorithms."""

    @staticmethod
    def uniform_cost(graph: WeightedGraph, start: Node, goal: Node) -> WeightedSearchResult | None:
        return _best_first_search(graph, start, goal, lambda _node, cost: cost)

    @staticmethod
    def greedy(
        graph: WeightedGraph,
        start: Node,
        goal: Node,
        heuristic: Heuristic | None = None,
    ) -> WeightedSearchResult | None:
        return _best_first_search(
            graph,
            start,
            goal,
            lambda node, _cost: _heuristic_value(heuristic, node, goal),
        )

    @staticmethod
    def a_star(
        graph: WeightedGraph,
        start: Node,
        goal: Node,
        heuristic: Heuristic | None = None,
    ) -> WeightedSearchResult | None:
        return _best_first_search(
            graph,
            start,
            goal,
            lambda node, cost: cost + _heuristic_value(heuristic, node, goal),
        )

    @staticmethod
    def search(
        graph: WeightedGraph,
        start: Node,
        goal: Node,
        method: str | WeightedSearchMethod = WeightedSearchMethod.UNIFORM_COST,
        heuristic: Heuristic | None = None,
    ) -> WeightedSearchResult | None:
        normalized_method = normalize_weighted_search_method(method)

        if normalized_method is WeightedSearchMethod.UNIFORM_COST:
            return WeightedSearchAlgorithms.uniform_cost(graph, start, goal)
        if normalized_method is WeightedSearchMethod.GREEDY:
            return WeightedSearchAlgorithms.greedy(graph, start, goal, heuristic)
        if normalized_method is WeightedSearchMethod.A_STAR:
            return WeightedSearchAlgorithms.a_star(graph, start, goal, heuristic)

        raise UnknownSearchMethodError(f"Unsupported weighted search method: {method}")


def _best_first_search(
    graph: WeightedGraph,
    start: Node,
    goal: Node,
    priority_for: callable,
) -> WeightedSearchResult | None:
    if start == goal:
        return WeightedSearchResult([start], 0.0)
    if start not in graph or goal not in graph:
        return None

    sequence = count()
    queue = [(0.0, next(sequence), 0.0, start, [start])]
    best_cost: dict[Node, float] = {start: 0.0}

    while queue:
        _priority, _sequence_id, cost, current, path = heapq.heappop(queue)
        if current == goal:
            return WeightedSearchResult(path, cost)

        if cost > best_cost.get(current, float("inf")):
            continue

        for neighbor, edge_cost in graph[current]:
            new_cost = cost + edge_cost
            if new_cost >= best_cost.get(neighbor, float("inf")):
                continue

            best_cost[neighbor] = new_cost
            priority = priority_for(neighbor, new_cost)
            heapq.heappush(queue, (priority, next(sequence), new_cost, neighbor, [*path, neighbor]))

    return None


def _heuristic_value(heuristic: Heuristic | None, node: Node, goal: Node) -> float:
    if heuristic is None:
        return 0.0

    value = heuristic.get(node, 0.0)
    if isinstance(value, Mapping):
        return float(value.get(goal, 0.0))
    return float(value)


class GraphValued:
    """Backward-compatible wrapper for the original weighted API."""

    def custo_uniforme(self, inicio: Node, fim: Node, nos, grafo):
        from waypy.graphs import build_weighted_graph

        result = WeightedSearchAlgorithms.uniform_cost(build_weighted_graph(nos, grafo), inicio, fim)
        return None if result is None else (result.path, result.cost)

    def greedy(self, inicio: Node, fim: Node, h, nos, grafo):
        from waypy.graphs import build_weighted_graph

        result = WeightedSearchAlgorithms.greedy(
            build_weighted_graph(nos, grafo),
            inicio,
            fim,
            _legacy_heuristic(h, nos, fim),
        )
        return None if result is None else (result.path, result.cost)

    def a_estrela(self, inicio: Node, fim: Node, h, nos, grafo):
        from waypy.graphs import build_weighted_graph

        result = WeightedSearchAlgorithms.a_star(
            build_weighted_graph(nos, grafo),
            inicio,
            fim,
            _legacy_heuristic(h, nos, fim),
        )
        return None if result is None else (result.path, result.cost)


def _legacy_heuristic(values, nodes, goal) -> dict[Node, float]:
    if isinstance(values, Mapping):
        return dict(values)

    node_list = list(nodes)
    if not values:
        return {}

    try:
        goal_index = node_list.index(goal)
        return {node: float(values[goal_index][index]) for index, node in enumerate(node_list)}
    except (ValueError, IndexError, TypeError):
        return {}
