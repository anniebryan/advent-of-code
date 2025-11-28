"""
Advent of Code 2020
Day 3: Toboggan Trajectory
"""

from math import prod


def num_trees(puzzle_input, right, down):
    width = len([i for i in puzzle_input[0] if i == "." or i == "#"])
    num_trees = 0
    y = 0
    for x in range(len(puzzle_input)):
        if x % down == 0:
            if puzzle_input[x][y] == "#":  # tree
                num_trees += 1
            y += right
            y %= width
    return num_trees


def solve_part_1(puzzle_input: list[str]):
    return num_trees(puzzle_input, 3,1)


def solve_part_2(puzzle_input: list[str]):
    all_ways = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    return prod([num_trees(puzzle_input, *way) for way in all_ways])
