# WayPy

WayPy is a small Python package for finding paths in directed graphs. It includes
classic unweighted and weighted search algorithms behind a simple object-oriented
API.

## Features

- Breadth-first search
- Depth-first search
- Limited-depth search
- Iterative deepening search
- Bidirectional search
- Uniform-cost search
- Greedy best-first search
- A* search
- Compatibility aliases for the original Portuguese API

## Installation

```bash
pip install WayPy
```

## Quick Start

```python
from waypy import Agent

agent = Agent.from_adjacency({
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D"],
    "D": [],
})

path = agent.find_path("A", "D", method="breadth_first")
print(path)
# ["A", "B", "D"]
```

## Weighted Graphs

```python
from waypy import Agent

agent = Agent.from_weighted_adjacency({
    "A": [("B", 1), ("C", 5)],
    "B": [("C", 1)],
    "C": [],
})

result = agent.find_weighted_path("A", "C", method="uniform_cost")
print(result.path)
# ["A", "B", "C"]
print(result.cost)
# 2.0
```

## Available Methods

Unweighted methods:

- `breadth_first`
- `depth_first`
- `limited_depth`
- `iterative_deepening`
- `bidirectional`

Weighted methods:

- `uniform_cost`
- `greedy`
- `a_star`

Legacy aliases such as `AMPLITUDE`, `PROFUNDIDADE`, `BIDIRECIONAL`,
`CUSTO_UNIFORME`, and `A_ESTRELA` are still accepted.

## Legacy API

The original class name remains available:

```python
from waypy import Agente

agent = Agente()
agent.nodes = ["A", "B", "C"]
agent.graphs = [["B"], ["C"], []]
agent.starting_points = ["A"]

path = agent.encontrar_ajuda_humanitaria("C", "AMPLITUDE")
print(path)
# ["A", "B", "C"]
```

New projects should prefer `Agent`, `find_path`, and `find_weighted_path`.

## Development

Install the package locally with test dependencies:

```bash
python -m pip install -e ".[test]"
```

Run the test suite:

```bash
python -m pytest
```

Build distribution artifacts:

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
```

Publish to PyPI:

```bash
python -m twine upload dist/*
```

## License

WayPy is distributed under the MIT License.
