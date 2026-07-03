"""Public object-oriented API for WayPy."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Hashable, Iterable, Mapping, Sequence

from waypy.graph_values import (
    Heuristic,
    WeightedSearchAlgorithms,
    WeightedSearchMethod,
    WeightedSearchResult,
    _legacy_heuristic,
)
from waypy.graphs import (
    Graph,
    WeightedGraph,
    build_graph,
    build_weighted_graph,
    ensure_graph,
    ensure_weighted_graph,
)
from waypy.methods import SearchAlgorithms, SearchMethod

Node = Hashable


@dataclass(slots=True)
class Agent:
    """High-level graph search facade."""

    graph: Graph = field(default_factory=dict)
    weighted_graph: WeightedGraph = field(default_factory=dict)
    heuristic: Heuristic | None = None
    starting_points: list[Node] = field(default_factory=list)
    arrival_points: list[Node] = field(default_factory=list)

    @classmethod
    def from_adjacency(
        cls,
        graph: Mapping[Node, Iterable[Node]],
        *,
        starting_points: Iterable[Node] | None = None,
        arrival_points: Iterable[Node] | None = None,
    ) -> "Agent":
        return cls(
            graph=ensure_graph(graph),
            starting_points=list(starting_points or []),
            arrival_points=list(arrival_points or []),
        )

    @classmethod
    def from_legacy_graph(
        cls,
        nodes: Iterable[Node],
        edges: Iterable[Iterable[Node]],
        *,
        starting_points: Iterable[Node] | None = None,
        arrival_points: Iterable[Node] | None = None,
    ) -> "Agent":
        return cls(
            graph=build_graph(nodes, edges),
            starting_points=list(starting_points or []),
            arrival_points=list(arrival_points or []),
        )

    @classmethod
    def from_weighted_adjacency(
        cls,
        graph: Mapping[Node, Iterable[Sequence[object]]],
        *,
        heuristic: Heuristic | None = None,
        starting_points: Iterable[Node] | None = None,
        arrival_points: Iterable[Node] | None = None,
    ) -> "Agent":
        return cls(
            weighted_graph=ensure_weighted_graph(graph),
            heuristic=heuristic,
            starting_points=list(starting_points or []),
            arrival_points=list(arrival_points or []),
        )

    @classmethod
    def from_legacy_weighted_graph(
        cls,
        nodes: Iterable[Node],
        edges: Iterable[Iterable[Sequence[object]]],
        *,
        heuristic: Heuristic | None = None,
        starting_points: Iterable[Node] | None = None,
        arrival_points: Iterable[Node] | None = None,
    ) -> "Agent":
        return cls(
            weighted_graph=build_weighted_graph(nodes, edges),
            heuristic=heuristic,
            starting_points=list(starting_points or []),
            arrival_points=list(arrival_points or []),
        )

    def set_legacy_graph(self, nodes: Iterable[Node], edges: Iterable[Iterable[Node]]) -> None:
        self.graph = build_graph(nodes, edges)

    def set_legacy_weighted_graph(self, nodes: Iterable[Node], edges: Iterable[Iterable[Sequence[object]]]) -> None:
        self.weighted_graph = build_weighted_graph(nodes, edges)

    def find_path(
        self,
        start: Node,
        goal: Node,
        method: str | SearchMethod = SearchMethod.BREADTH_FIRST,
        *,
        limit: int | None = None,
    ) -> list[Node] | None:
        return SearchAlgorithms.search(self.graph, start, goal, method, limit)

    def find_weighted_path(
        self,
        start: Node,
        goal: Node,
        method: str | WeightedSearchMethod = WeightedSearchMethod.UNIFORM_COST,
        *,
        heuristic: Heuristic | None = None,
    ) -> WeightedSearchResult | None:
        return WeightedSearchAlgorithms.search(
            self.weighted_graph,
            start,
            goal,
            method,
            heuristic if heuristic is not None else self.heuristic,
        )

    def find_best_path_from_sources(
        self,
        sources: Iterable[Node],
        goal: Node,
        method: str | SearchMethod = SearchMethod.BREADTH_FIRST,
        *,
        limit: int | None = None,
    ) -> list[Node] | None:
        paths = (
            self.find_path(source, goal, method, limit=limit)
            for source in sources
        )
        return _shortest_path(paths)

    def find_best_path_to_targets(
        self,
        start: Node,
        targets: Iterable[Node],
        method: str | SearchMethod = SearchMethod.BREADTH_FIRST,
        *,
        limit: int | None = None,
    ) -> list[Node] | None:
        paths = (
            self.find_path(start, target, method, limit=limit)
            for target in targets
        )
        return _shortest_path(paths)

    def find_lowest_cost_from_sources(
        self,
        sources: Iterable[Node],
        goal: Node,
        method: str | WeightedSearchMethod = WeightedSearchMethod.UNIFORM_COST,
        *,
        heuristic: Heuristic | None = None,
    ) -> WeightedSearchResult | None:
        results = (
            self.find_weighted_path(source, goal, method, heuristic=heuristic)
            for source in sources
        )
        return _lowest_cost_result(results)

    def find_lowest_cost_to_targets(
        self,
        start: Node,
        targets: Iterable[Node],
        method: str | WeightedSearchMethod = WeightedSearchMethod.UNIFORM_COST,
        *,
        heuristic: Heuristic | None = None,
    ) -> WeightedSearchResult | None:
        results = (
            self.find_weighted_path(start, target, method, heuristic=heuristic)
            for target in targets
        )
        return _lowest_cost_result(results)

    def join_paths(self, first_path: Sequence[Node], second_path: Sequence[Node]) -> list[Node]:
        if not first_path:
            return list(second_path)
        if not second_path:
            return list(first_path)
        return [*first_path, *second_path[1:]]


class Agente(Agent):
    """Compatibility alias for the original Portuguese class name."""

    methods = [
        "AMPLITUDE",
        "PROFUNDIDADE",
        "PROFUNDIDADE LIMITADA",
        "APROFUNDAMENTO ITERATIVO",
        "BIDIRECIONAL",
        "A_ESTRELA",
        "GREEDY",
        "CUSTO_UNIFORME",
    ]

    def __init__(self):
        super().__init__()
        self.nodes: list[Node] = []
        self.graphs: list[list[Node]] = []

    def encontrar_atendimento(self, cidade_final, metodo, limite=False):
        self.set_legacy_graph(self.nodes, self.graphs)
        return self.find_best_path_to_targets(
            str(cidade_final).upper(),
            self.arrival_points,
            metodo,
            limit=limite if isinstance(limite, int) else None,
        )

    def encontrar_ajuda_humanitaria(self, cidade_final, metodo, limite=False):
        self.set_legacy_graph(self.nodes, self.graphs)
        return self.find_best_path_from_sources(
            self.starting_points,
            str(cidade_final).upper(),
            metodo,
            limit=limite if isinstance(limite, int) else None,
        )

    def valued_graph(self, cidade_final, metodo, level):
        points = self.starting_points if level == 1 else self.arrival_points
        self.set_legacy_weighted_graph(self.nodes, self.weighted_graph)
        self.heuristic = _legacy_heuristic(self.heuristic, self.nodes, str(cidade_final).upper())

        if level == 1:
            result = self.find_lowest_cost_from_sources(points, str(cidade_final).upper(), metodo)
        else:
            result = self.find_lowest_cost_to_targets(str(cidade_final).upper(), points, metodo)

        return None if result is None else result.path

    def unifica_caminho(self, rota_AH, rota_At):
        return self.join_paths(rota_AH, rota_At)

    def amplitude(self, inicio, fim, nos, grafo):
        return SearchAlgorithms.breadth_first(build_graph(nos, grafo), inicio, fim)

    def profundidade(self, inicio, fim, nos, grafo):
        return SearchAlgorithms.depth_first(build_graph(nos, grafo), inicio, fim)

    def profundidade_limitada(self, inicio, fim, limite, nos, grafo):
        return SearchAlgorithms.limited_depth(build_graph(nos, grafo), inicio, fim, limite)

    def aprofundamento_iterativo(self, inicio, fim, nos, grafo):
        return SearchAlgorithms.iterative_deepening(build_graph(nos, grafo), inicio, fim)

    def bidirecional(self, inicio, fim, nos, grafo):
        return SearchAlgorithms.bidirectional(build_graph(nos, grafo), inicio, fim)


def _shortest_path(paths: Iterable[list[Node] | None]) -> list[Node] | None:
    valid_paths = [path for path in paths if path is not None]
    if not valid_paths:
        return None
    return min(valid_paths, key=len)


def _lowest_cost_result(results: Iterable[WeightedSearchResult | None]) -> WeightedSearchResult | None:
    valid_results = [result for result in results if result is not None]
    if not valid_results:
        return None
    return min(valid_results, key=lambda result: result.cost)
