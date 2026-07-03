import pytest

from waypy.exceptions import UnknownSearchMethodError
from waypy.methods import SearchAlgorithms, SearchMethod


GRAPH = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D"],
    "D": ["E"],
    "E": [],
    "F": [],
}


def test_breadth_first_finds_the_shortest_path_by_edges():
    assert SearchAlgorithms.breadth_first(GRAPH, "A", "E") == ["A", "B", "D", "E"]


def test_depth_first_returns_a_valid_depth_first_path():
    assert SearchAlgorithms.depth_first(GRAPH, "A", "E") == ["A", "B", "D", "E"]


def test_limited_depth_respects_the_limit():
    assert SearchAlgorithms.limited_depth(GRAPH, "A", "E", 2) is None
    assert SearchAlgorithms.limited_depth(GRAPH, "A", "E", 3) == ["A", "B", "D", "E"]


def test_iterative_deepening_finds_a_path():
    assert SearchAlgorithms.iterative_deepening(GRAPH, "A", "E") == ["A", "B", "D", "E"]


def test_bidirectional_finds_a_path():
    assert SearchAlgorithms.bidirectional(GRAPH, "A", "E") == ["A", "B", "D", "E"]


def test_start_equal_goal_returns_single_node_path():
    assert SearchAlgorithms.search(GRAPH, "A", "A", SearchMethod.BREADTH_FIRST) == ["A"]


def test_missing_path_returns_none():
    assert SearchAlgorithms.breadth_first(GRAPH, "E", "A") is None


def test_portuguese_method_aliases_are_supported():
    assert SearchAlgorithms.search(GRAPH, "A", "E", "AMPLITUDE") == ["A", "B", "D", "E"]


def test_unknown_method_raises_a_clear_error():
    with pytest.raises(UnknownSearchMethodError, match="Unsupported"):
        SearchAlgorithms.search(GRAPH, "A", "E", "not-a-method")
