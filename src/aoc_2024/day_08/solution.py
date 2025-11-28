"""
Advent of Code 2024
Day 8: Resonant Collinearity
"""

from collections import defaultdict


def parse_input(puzzle_input: list[str]):
    antenna_locs = defaultdict(set)
    for i, row in enumerate(puzzle_input):
        for j, val in enumerate(row):
            if val != ".":
                antenna_locs[val].add((i, j))
    puzzle_size = (len(puzzle_input), len(puzzle_input[0]))
    return antenna_locs, puzzle_size


def in_bounds(antinode_loc, puzzle_size):
    i, j = antinode_loc
    height, width = puzzle_size
    return 0 <= i < height and 0 <= j < width


def get_antinode_locs(antenna_locs, puzzle_size, part_2):
    antinode_locs = set()
    for antennas in antenna_locs.values():
        for antenna_a in antennas:
            for antenna_b in antennas - {antenna_a}:
                diff_i = antenna_a[0] - antenna_b[0]
                diff_j = antenna_a[1] - antenna_b[1]
                if part_2:
                    new_antinode_loc = antenna_a
                    while in_bounds(new_antinode_loc, puzzle_size):
                        antinode_locs.add(new_antinode_loc)
                        new_antinode_loc = (new_antinode_loc[0] + diff_i, new_antinode_loc[1] + diff_j)
                    new_antinode_loc = antenna_b
                    while in_bounds(new_antinode_loc, puzzle_size):
                        antinode_locs.add(new_antinode_loc)
                        new_antinode_loc = (new_antinode_loc[0] - diff_i, new_antinode_loc[1] - diff_j)
                else:
                    antinode_1 = (antenna_a[0] + diff_i, antenna_a[1] + diff_j)
                    antinode_2 = (antenna_b[0] - diff_i, antenna_b[1] - diff_j)
                    if in_bounds(antinode_1, puzzle_size):
                        antinode_locs.add(antinode_1)
                    if in_bounds(antinode_2, puzzle_size):
                        antinode_locs.add(antinode_2)
    return antinode_locs


def solve_part_1(puzzle_input: list[str]):
    antenna_locs, puzzle_size = parse_input(puzzle_input)
    return len(get_antinode_locs(antenna_locs, puzzle_size, False))


def solve_part_2(puzzle_input: list[str]):
    antenna_locs, puzzle_size = parse_input(puzzle_input)
    return len(get_antinode_locs(antenna_locs, puzzle_size, True))
