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
    grid = parse_input(puzzle_input, True)
    start = grid.where("S")[0]
    if grid.width != grid.height:
        raise NotImplementedError("Solution does not work for non-square grids")

    NUM_STEPS = 26501365
    dist_to_border = grid.width // 2
    remaining_steps = NUM_STEPS - dist_to_border
    num_plots = remaining_steps // grid.width
    if remaining_steps % num_plots != 0:
        raise NotImplementedError("Solution does not work when number of steps is not whole number of plots")

    # Note: the number of plots we can reach happens to follow a quadratic curve
    num_reachable = {}
    for num_grids in range(3):
        max_path_length = num_grids * grid.width + grid.width // 2
        dists = grid.dijkstra(start, max_path_length=max_path_length, allow_wrap_around=True)
        num_reachable[num_grids] = len([v for v in dists.values() if v % 2 == max_path_length % 2])
    n0, n1, n2 = num_reachable[0], num_reachable[1], num_reachable[2]

    a = (n2 - 2 * n1 + n0) // 2
    b = n1 - n0 - a
    c = n0

    return a * num_plots ** 2 + b * num_plots + c
