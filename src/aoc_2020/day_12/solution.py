"""
Advent of Code 2020
Day 12: Rain Risk
"""

import os
from pathlib import Path

import click


def get_instructions(puzzle_input):
    return [(line[0], int(line[1:])) for line in puzzle_input]


def process_instruction(instruction, direction, x, y):
    action, val = instruction[0], instruction[1]
    if action == 'N' or (action == 'F' and direction == 90):
        return direction, x, y + val
    if action == 'S' or (action == 'F' and direction == 270):
        return direction, x, y - val
    if action == 'E' or (action == 'F' and direction == 0):
        return direction, x + val, y
    if action == 'W' or (action == 'F' and direction == 180):
        return direction, x - val, y
    if action == 'L':
        return (direction + val) % 360, x, y
    if action == 'R':
        return (direction - val) % 360, x, y
    raise NotImplementedError


def process_waypoint(instruction, x, y, way_x, way_y):
    action, val = instruction[0], instruction[1]
    if action == 'N':
        return x, y, way_x, way_y + val
    if action == 'S':
        return x, y, way_x, way_y - val
    if action == 'E':
        return x, y, way_x + val, way_y
    if action == 'W':
        return x, y, way_x - val, way_y
    if (action == 'L' and val == 90)  or (action == 'R' and val == 270):
        return x, y, -way_y, way_x
    if (action == 'L' and val == 270) or (action == 'R' and val == 90):
        return x, y, way_y, -way_x
    if (action == 'L' or action == 'R') and val == 180:
        return x, y, -way_x, -way_y
    if action == 'F':
        return x + way_x * val, y + way_y * val, way_x, way_y
    raise NotImplementedError


def process_all_instructions(puzzle_input, part_one):
    instructions = get_instructions(puzzle_input)
    x, y = 0, 0
    if part_one:
        direction = 0
        for instruction in instructions:
            direction, x, y = process_instruction(instruction, direction, x, y)
    else:
        way_x, way_y = 10, 1
        for instruction in instructions:
            x, y, way_x, way_y = process_waypoint(instruction, x, y, way_x, way_y)
    return x, y


def manhattan_distance(x, y):
    return abs(x) + abs(y)


def solve_part_1(puzzle_input: list[str]):
    final_x, final_y = process_all_instructions(puzzle_input, True)
    return manhattan_distance(final_x, final_y)


def solve_part_2(puzzle_input: list[str]):
    final_x, final_y = process_all_instructions(puzzle_input, False)
    return manhattan_distance(final_x, final_y)
