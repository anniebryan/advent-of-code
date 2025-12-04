"""
Advent of Code 2025
Day 4: Printing Department
"""

from aoc_utils import Grid


def parse_input(puzzle_input: list[str], part_2: bool) -> Grid:
    return Grid(puzzle_input)


def solve_part_1(puzzle_input: list[str]):
    g = parse_input(puzzle_input, False)

    num_accessible = 0
    for (x, y) in g:
        num_adj_rolls = 0

        if g.at(x, y) != "@":
            continue

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # (x, y) is not a neighbor of itself
                nx, ny = x + dx, y + dy
                if g.in_bounds(nx, ny) and g.at(nx, ny) == "@":
                    num_adj_rolls += 1
        if num_adj_rolls < 4:
            num_accessible += 1
    return num_accessible


def solve_part_2(puzzle_input: list[str]):
    _ = parse_input(puzzle_input, True)
    return
