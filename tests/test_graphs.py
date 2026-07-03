import pytest

from waypy.exceptions import InvalidGraphError
from waypy.graphs import build_graph, build_weighted_graph, ensure_graph


def test_build_graph_from_legacy_parallel_lists():
    graph = build_graph(["A", "B", "C"], [["B"], ["C"], []])

    assert graph == {"A": ["B"], "B": ["C"], "C": []}


def test_build_graph_rejects_unknown_neighbors():
    with pytest.raises(InvalidGraphError, match="Unknown neighbor"):
        build_graph(["A"], [["B"]])


def test_build_graph_rejects_duplicate_nodes():
    with pytest.raises(InvalidGraphError, match="duplicates"):
        build_graph(["A", "A"], [[], []])


def test_ensure_graph_returns_a_defensive_copy():
    source = {"A": ["B"], "B": []}
    graph = ensure_graph(source)

    source["A"].append("A")

    assert graph == {"A": ["B"], "B": []}


def test_build_weighted_graph_rejects_negative_costs():
    with pytest.raises(InvalidGraphError, match="negative"):
        build_weighted_graph(["A", "B"], [[("B", -1)], []])


def test_build_weighted_graph_normalizes_costs_to_float():
    graph = build_weighted_graph(["A", "B"], [[("B", 2)], []])

    assert graph == {"A": [("B", 2.0)], "B": []}
