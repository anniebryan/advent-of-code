"""
Advent of Code 2021
Day 2: Dive!
"""

import os
from pathlib import Path

import click

forward = lambda x: x[0] == 'forward'
up = lambda x: x[0] == 'up'
down = lambda x: x[0] == 'down'
amount = lambda x: x[1]


def get_commands(puzzle_input):
    return [(n.split(' ')[0], int(n.split(' ')[1])) for n in puzzle_input]


def solve_part_1(puzzle_input: list[str]):
    commands = get_commands(puzzle_input)
    horiz = sum(map(amount, filter(forward, commands)))
    depth = sum(map(amount, filter(down, commands))) - sum(map(amount, filter(up, commands)))
    return horiz * depth


def solve_part_2(puzzle_input: list[str]):
    commands = get_commands(puzzle_input)
    horiz = sum(map(amount, filter(forward, commands)))
    depth, aim = 0, 0
    for x in commands:
        if forward(x):
            depth += aim * amount(x)
        elif down(x):
            aim += amount(x)
        elif up(x):
            aim -= amount(x)
    return horiz * depth
