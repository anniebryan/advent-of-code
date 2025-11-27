"""
Advent of Code 2024
Day 23: LAN Party
"""

import os
from pathlib import Path

import click

from utils import DirectedGraph


def parse_input(puzzle_input: list[str]) -> DirectedGraph:
    g = DirectedGraph()
    for line in puzzle_input:
        a, b = line.split("-")
        g.insert_edge(a, b)
        g.insert_edge(b, a)
    return g


def get_cycles(g: DirectedGraph, n: int) -> set[tuple[str, ...]]:
    def dfs(path: list[str], start_node: str, visited: set[str]):
        node = path[-1]
        if len(path) == n and start_node in g.neighbors(node):
            yield tuple(sorted(path))

        if len(path) < n:
            for neighbor in g.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    yield from dfs(path + [neighbor], start_node, visited)
                    visited.remove(neighbor)

    cycles = set()
    for start_node in g.graph:
        if start_node.startswith("t"):
            for cycle in dfs([start_node], start_node, set()):
                cycles.add(cycle)
    return cycles

def get_largest_fully_connected_component_helper(g: DirectedGraph, component: set[str], memo: dict[str, set[str]]) -> set[str]:
    component_str = ",".join(sorted(component))
    if component_str in memo:
        return memo[component_str]

    largest_component = component
    for n in set(g.graph) - component:
        if component - g.neighbors(n) == set():
            # n is neighbors with all items already in component
            new_component = get_largest_fully_connected_component_helper(g, component | {n}, memo)
            if len(new_component) > len(largest_component):
                largest_component = new_component

    memo[component_str] = largest_component
    return largest_component


def get_largest_fully_connected_component(g: DirectedGraph) -> set[str]:
    largest_component = set()
    memo = {}
    for start_node in g.graph:
        component = get_largest_fully_connected_component_helper(g, {start_node}, memo)
        if len(component) > len(largest_component):
            largest_component = component

    return largest_component


def solve_part_1(puzzle_input: list[str]):
    g = parse_input(puzzle_input)
    return len(get_cycles(g, 3))


# TODO speedup
def solve_part_2(puzzle_input: list[str]):
    g = parse_input(puzzle_input)
    return ",".join(sorted(get_largest_fully_connected_component(g)))


@click.command()
@click.option("-se", "--skip_example", is_flag=True, default=False)
@click.option("-sp", "--skip_puzzle", is_flag=True, default=False)
def main(skip_example: bool = False, skip_puzzle: bool = False) -> None:
    base_dir = Path(__file__).parent
    example_files = sorted([fn for fn in os.listdir(base_dir) if fn.endswith(".txt") and "example" in fn])

    def _run_solution(filename: str, display_name: str):
        print(f"--- {display_name} ---")

        if not (filepath := (base_dir / filename)).exists():
            print(f"{filename} not found.")
            return

        with open(filepath) as file:
            puzzle_input = [line.strip("\n") for line in file]
            print(f"Part 1: {solve_part_1(puzzle_input)}")
            print(f"Part 2: {solve_part_2(puzzle_input)}")
        return

    if not skip_example:
        if len(example_files) < 2:
            _run_solution("example.txt", "Example")
        else:
            for i, filename in enumerate(example_files):
                _run_solution(filename, f"Example {i + 1}")

    if not skip_puzzle:
        _run_solution("puzzle.txt", "Puzzle")


if __name__ == "__main__":
    main()
