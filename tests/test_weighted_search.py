import pytest

from waypy.exceptions import UnknownSearchMethodError
from waypy.graph_values import WeightedSearchAlgorithms


GRAPH = {
    "A": [("B", 1.0), ("C", 5.0)],
    "B": [("C", 1.0), ("D", 4.0)],
    "C": [("D", 1.0)],
    "D": [],
}


def test_uniform_cost_finds_lowest_cost_path():
    result = WeightedSearchAlgorithms.uniform_cost(GRAPH, "A", "D")

    assert result.path == ["A", "B", "C", "D"]
    assert result.cost == 3.0


def test_a_star_uses_heuristics_and_returns_start_to_goal_path():
    heuristic = {"A": 3.0, "B": 2.0, "C": 1.0, "D": 0.0}

    result = WeightedSearchAlgorithms.a_star(GRAPH, "A", "D", heuristic)

    assert result.path == ["A", "B", "C", "D"]
    assert result.cost == 3.0


def test_greedy_returns_a_reachable_path_with_cost():
    heuristic = {"A": 3.0, "B": 2.0, "C": 0.0, "D": 0.0}

    result = WeightedSearchAlgorithms.greedy(GRAPH, "A", "D", heuristic)

    assert result.path[0] == "A"
    assert result.path[-1] == "D"
    assert result.cost > 0


def test_weighted_search_returns_none_when_goal_is_unreachable():
    assert WeightedSearchAlgorithms.uniform_cost(GRAPH, "D", "A") is None


def test_weighted_search_accepts_portuguese_aliases():
    result = WeightedSearchAlgorithms.search(GRAPH, "A", "D", "CUSTO_UNIFORME")

    assert result.path == ["A", "B", "C", "D"]
    assert result.cost == 3.0


def test_unknown_weighted_method_raises_a_clear_error():
    with pytest.raises(UnknownSearchMethodError, match="Unsupported"):
        WeightedSearchAlgorithms.search(GRAPH, "A", "D", "not-a-method")
