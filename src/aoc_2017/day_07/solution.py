"""
Advent of Code 2017
Day 7: Recursive Circus
"""

from collections import Counter

from aoc_utils import DirectedGraph


def parse_input(puzzle_input: list[str], part_2: bool):
    g = DirectedGraph()
    tower_weights = {}

    for line in puzzle_input:
        name, weight, *remaining = line.split()
        weight = int(weight.removeprefix("(").removesuffix(")"))
        tower_weights[name] = weight
        if remaining:
            for tower in remaining[1:]:
                g.insert_edge(name, tower.strip().replace(",", ""))

    return g, tower_weights


def _get_root_tower(g: DirectedGraph, tower_weights: dict[str, int]) -> str:
    all_towers = set(tower_weights)
    roots = []
    for t in all_towers:
        if not g.incoming_neighbors(t):
            roots.append(t)
    assert len(roots) == 1
    return roots[0]


def solve_part_1(puzzle_input: list[str]):
    g, tower_weights = parse_input(puzzle_input, False)
    return _get_root_tower(g, tower_weights)


def _get_total_tower_weight(tower: str, g: DirectedGraph, tower_weights: dict[str, int]) -> int:
    weight = tower_weights[tower]
    for n in g.outgoing_neighbors(tower):
        weight += _get_total_tower_weight(n, g, tower_weights)
    return weight


def _find_corrected_weight(tower: str, g: DirectedGraph, tower_weights: dict[str, int]) -> tuple[int, int | None]:
    child_weights = {}
    for child in g.outgoing_neighbors(tower):
        total_weight, corrected_weight = _find_corrected_weight(child, g, tower_weights)
        if corrected_weight is not None:
            return tower_weights[tower] + sum(child_weights.values()), corrected_weight
        child_weights[child] = total_weight

    if child_weights:
        weight_counts = Counter(child_weights.values())
        if len(weight_counts) > 1:
            expected_weight, _ = weight_counts.most_common(1)[0]
            incorrect_weight = next(weight for weight, count in weight_counts.items() if count == 1)
            incorrect_tower = next(child for child, weight in child_weights.items() if weight == incorrect_weight)
            corrected_weight = tower_weights[incorrect_tower] + expected_weight - incorrect_weight
            return (tower_weights[tower] + sum(child_weights.values()), corrected_weight)

    return tower_weights[tower] + sum(child_weights.values()), None


def solve_part_2(puzzle_input: list[str]):
    g, tower_weights = parse_input(puzzle_input, True)
    root = _get_root_tower(g, tower_weights)
    _, corrected_weight = _find_corrected_weight(root, g, tower_weights)
    return corrected_weight
