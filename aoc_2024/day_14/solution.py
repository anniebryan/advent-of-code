"""
Advent of Code 2024
Day 14: Restroom Redoubt
"""

import click
import os
import pathlib
import regex as re
from math import prod
from collections import defaultdict


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


@click.command()
@click.option("-se", "--skip_example", is_flag=True, default=False)
@click.option("-sp", "--skip_puzzle", is_flag=True, default=False)
def main(skip_example: bool = False, skip_puzzle: bool = False) -> None:
    base_dir = pathlib.Path(__file__).parent
    example_files = sorted([fn for fn in os.listdir(base_dir) if fn.endswith(".txt") and "example" in fn])

    def _run_solution(filename: str, display_name: str):
        print(f"--- {display_name} ---")

        if not (filepath := (base_dir / filename)).exists():
            print(f"{filename} not found.")
            return

        with open(filepath) as file:
            puzzle_input = [line.strip("\n") for line in file]
            print(f"Part 1: {solve_part_1(puzzle_input)}")
            print(f"Part 2: {solve_part_2(puzzle_input)}")
        return

    if not skip_example:
        if len(example_files) < 2:
            _run_solution("example.txt", "Example")
        else:
            for i, filename in enumerate(example_files):
                _run_solution(filename, f"Example {i + 1}")

    if not skip_puzzle:
        _run_solution("puzzle.txt", "Puzzle")


if __name__ == "__main__":
    main()
