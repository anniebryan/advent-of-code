"""
Advent of Code 2017
Day 3: Spiral Memory
"""

from aoc_utils import Grid


def parse_input(puzzle_input: list[str], part_2: bool):
    return int(puzzle_input[0])


def solve_part_1(puzzle_input: list[str]):
    num = parse_input(puzzle_input, False)

    g = Grid()
    curr_x, curr_y, curr_num = 0, 0, 1
    g.set(curr_x, curr_y, curr_num)

    dx, dy = 1, 0  # right
    prev_width, prev_height = g.width, g.height
    while curr_num < num:
        curr_x += dx
        curr_y += dy
        curr_num += 1
        g.set(curr_x, curr_y, curr_num)

        if g.width > prev_width or g.height > prev_height:
            dx, dy = -dy, dx # turn left

        prev_width, prev_height = g.width, g.height

    return abs(curr_x) + abs(curr_y)


def solve_part_2(puzzle_input: list[str]):
    num = parse_input(puzzle_input, True)

    g = Grid()
    curr_x, curr_y, curr_num = 0, 0, 1
    g.set(curr_x, curr_y, curr_num)

    dx, dy = 1, 0  # right
    prev_width, prev_height = g.width, g.height
    while curr_num < num:
        curr_x += dx
        curr_y += dy
        neighbors = [int(g.at(*n)) for n in g.neighbors((curr_x, curr_y), include_diagonals=True)]
        curr_num = sum(neighbors)
        g.set(curr_x, curr_y, curr_num)

        if g.width > prev_width or g.height > prev_height:
            dx, dy = -dy, dx # turn left

        prev_width, prev_height = g.width, g.height

    return curr_num
