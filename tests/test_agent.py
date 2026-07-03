from waypy import Agent, Agente
from waypy.graph_values import WeightedSearchResult


def test_agent_builds_from_legacy_graph_and_finds_paths():
    agent = Agent.from_legacy_graph(
        ["A", "B", "C"],
        [["B"], ["C"], []],
        starting_points=["A"],
        arrival_points=["C"],
    )

    assert agent.find_path("A", "C") == ["A", "B", "C"]
    assert agent.find_best_path_from_sources(agent.starting_points, "C") == ["A", "B", "C"]
    assert agent.find_best_path_to_targets("A", agent.arrival_points) == ["A", "B", "C"]


def test_agent_finds_weighted_paths():
    agent = Agent.from_legacy_weighted_graph(
        ["A", "B", "C"],
        [[("B", 1), ("C", 5)], [("C", 1)], []],
        starting_points=["A"],
    )

    result = agent.find_weighted_path("A", "C")

    assert result == WeightedSearchResult(["A", "B", "C"], 2.0)


def test_join_paths_removes_the_duplicate_meeting_node():
    agent = Agent()

    assert agent.join_paths(["A", "B"], ["B", "C"]) == ["A", "B", "C"]


def test_legacy_agent_has_isolated_mutable_state():
    first = Agente()
    second = Agente()

    first.nodes.append("A")

    assert second.nodes == []


def test_legacy_unweighted_api_still_works_with_english_return_values():
    agent = Agente()
    agent.nodes = ["A", "B", "C"]
    agent.graphs = [["B"], ["C"], []]
    agent.starting_points = ["A"]

    assert agent.amplitude("A", "C", agent.nodes, agent.graphs) == ["A", "B", "C"]
    assert agent.encontrar_ajuda_humanitaria("C", "AMPLITUDE") == ["A", "B", "C"]


def test_legacy_uniform_cost_branch_is_reachable():
    agent = Agente()
    agent.nodes = ["A", "B", "C"]
    agent.weighted_graph = [[("B", 1), ("C", 5)], [("C", 1)], []]
    agent.starting_points = ["A"]

    assert agent.valued_graph("C", "CUSTO_UNIFORME", 1) == ["A", "B", "C"]
