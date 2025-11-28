"""
Advent of Code 2024
Day 11: Plutonian Pebbles
"""

import os
from pathlib import Path

import click


def parse_input(puzzle_input: list[str]):
    return [int(n) for n in puzzle_input[0].split()]


def get_num_stones(val: int, num_blinks: int, memo) -> int:
    if (val, num_blinks) in memo:
        return memo[(val, num_blinks)]

    if num_blinks == 0:
        memo[(val, num_blinks)] = 1
        return 1

    if val == 0:
        memo[(val, num_blinks)] = get_num_stones(1, num_blinks - 1, memo)
        return memo[(val, num_blinks)]

    if (l := len(str(val))) % 2 == 0:
        m = int(l / 2)
        left = get_num_stones(int(str(val)[:m]), num_blinks - 1, memo)
        right = get_num_stones(int(str(val)[m:]), num_blinks - 1, memo)
        memo[(val, num_blinks)] = left + right
        return memo[(val, num_blinks)]

    memo[(val, num_blinks)] = get_num_stones(val * 2024, num_blinks - 1, memo)
    return memo[(val, num_blinks)]


def solve(vals: list[int], num_blinks: int) -> int:
    tot_stones = 0
    memo = {}
    for val in vals:
        tot_stones += get_num_stones(val, num_blinks, memo)
    return tot_stones


def solve_part_1(puzzle_input: list[str]):
    vals = parse_input(puzzle_input)
    return solve(vals, 25)


def solve_part_2(puzzle_input: list[str]):
    vals = parse_input(puzzle_input)
    return solve(vals, 75)
