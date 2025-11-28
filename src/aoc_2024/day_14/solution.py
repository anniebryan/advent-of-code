"""
Advent of Code 2024
Day 14: Restroom Redoubt
"""

import os
from collections import defaultdict
from math import prod
from pathlib import Path

import click
import regex as re


def parse_input(puzzle_input: list[str]):
    width = int(re.match(r"width=(?P<width>\d+)", puzzle_input[0]).group('width'))
    height = int(re.match(r"height=(?P<height>\d+)", puzzle_input[1]).group('height'))
    run_part_2 = puzzle_input[2] == "True"
    robots = set()
    for line in puzzle_input[3:]:
        match = re.match(r"p=(?P<px>-?\d+),(?P<py>-?\d+) v=(?P<vx>-?\d+),(?P<vy>-?\d+)", line)
        pos = (int(match.group("px")), int(match.group("py")))
        vel = (int(match.group("vx")), int(match.group("vy")))
        robots.add((pos, vel))
    return robots, width, height, run_part_2


def print_robots(robots, width, height):
    robot_locs = defaultdict(int)
    for robot in robots:
        (i, j), vel = robot
        robot_locs[(i, j)] += 1

    output = []
    for j in range(height):
        s = []
        for i in range(width):
            if robot_locs[(i, j)] > 0:
                s.append("X")
            else:
                s.append(" ")
        output.append("".join(s))
    print("\n".join(output))


def timestamp(robots: set[tuple[tuple[int, int], tuple[int, int]]],
              width: int,
              height: int) -> set:
    new_robots = set()
    for (pos, vel) in robots:
        px, py = pos
        vx, vy = vel
        new_x = (px + vx) % width
        new_y = (py + vy) % height
        new_robots.add(((new_x, new_y), vel))
    return new_robots


def in_top_half(j: int, height: int) -> bool:
    return j < height // 2


def in_left_half(i: int, width: int) -> bool:
    return i < width // 2


def calc_safety_score(robots: set[tuple[tuple[int, int], tuple[int, int]]],
                      width: int,
                      height: int) -> set:
    quadrants = defaultdict(int)
    for robot in robots:
        (i, j), _ = robot
        if j != height // 2 and i != width // 2:
            q = 2 * int(in_left_half(i, width)) + int(in_top_half(j, height))
            quadrants[q] += 1
    return prod(quadrants.values())


def overlap(robots):
    seen = set()
    for pos, _ in robots:
        if pos in seen:
            return True
        seen.add(pos)
    return False


def solve_part_1(puzzle_input: list[str]):
    robots, width, height, _ = parse_input(puzzle_input)
    for _ in range(100):
        robots = timestamp(robots, width, height)
    return calc_safety_score(robots, width, height)


def solve_part_2(puzzle_input: list[str]):
    robots, width, height, run_part_2 = parse_input(puzzle_input)
    if not run_part_2:
        return
    i = 0
    while overlap(robots):
        i += 1
        robots = timestamp(robots, width, height)
    print_robots(robots, width, height)
    return i
