"""
Advent of Code 2025
Day 11: Reactor
"""

from aoc_utils import DirectedWeightedGraph


def parse_input(puzzle_input: list[str], part_2: bool):
    device_graph = DirectedWeightedGraph()
    for line in puzzle_input:
        d, outputs = line.split(":")
        for o in outputs.strip().split():
            device_graph.insert_edge(d, o)
    return device_graph


def solve_part_1(puzzle_input: list[str]):
    device_graph = parse_input(puzzle_input, False)
    return len(list(device_graph.all_unique_paths("you", "out")))


def _solve_part_2_helper(
        device_graph: DirectedWeightedGraph,
        node: str,
        dac: bool = False,
        fft: bool = False,
        memo: dict = {},
) -> int:
    memo_key = (node, dac, fft)
    if memo_key not in memo:
        if node == "out" and dac and fft:
            memo[memo_key] = 1
        else:
            num_paths = 0
            for n in device_graph.neighbors[node]:
                num_paths += _solve_part_2_helper(
                    device_graph,
                    n,
                    dac or n == "dac",
                    fft or n == "fft",
                    memo,
                )
            memo[memo_key] = num_paths
    return memo[memo_key]


def solve_part_2(puzzle_input: list[str]):
    device_graph = parse_input(puzzle_input, True)
    return _solve_part_2_helper(device_graph, "svr", memo={})
