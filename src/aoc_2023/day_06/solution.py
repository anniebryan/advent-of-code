"""
Advent of Code 2023
Day 6: Wait For It
"""

import os
from math import prod
from pathlib import Path

import click


def parse_input(puzzle_input: list[str], part_2: bool):
    if part_2:
        times = [int("".join(puzzle_input[0].split()[1:]))]
        dists = [int("".join(puzzle_input[1].split()[1:]))]
    else:
        times = [int(d) for d in puzzle_input[0].split()[1:]]
        dists = [int(d) for d in puzzle_input[1].split()[1:]]
    return list(zip(times, dists))


def num_ways_to_win(time, dist_record):
    num_ways = 0
    for num_ms in range(time + 1):
        distance_traveled = num_ms * (time - num_ms)
        if distance_traveled > dist_record:
            num_ways += 1
    return num_ways


def solve_part_1(puzzle_input: list[str]):
    races = parse_input(puzzle_input, False)
    all_num_ways = []
    for time, dist_record in races:
        all_num_ways.append(num_ways_to_win(time, dist_record))
    return prod(all_num_ways)


def solve_part_2(puzzle_input: list[str]):
    time, dist_record = parse_input(puzzle_input, True)[0]
    return num_ways_to_win(time, dist_record)
