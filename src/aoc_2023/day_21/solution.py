"""
Advent of Code 2023
Day 21: Step Counter
"""

from aoc_utils import Grid


def parse_input(puzzle_input: list[str], part_2: bool):
    return Grid.from_puzzle_input(puzzle_input)


def solve_part_1(puzzle_input: list[str]):
    grid = parse_input(puzzle_input, False)
    start = grid.where("S")[0]
    dists = grid.dijkstra(start)
    num_reachable = 0
    num_steps = 64
    for _, v in dists.items():
        if v in {num_steps - 2 * i for i in range(num_steps // 2 + 1)}:
            num_reachable += 1
    return num_reachable


def solve_part_2(puzzle_input: list[str]):
    _ = parse_input(puzzle_input, True)
    raise NotImplementedError