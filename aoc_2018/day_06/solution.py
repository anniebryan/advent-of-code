"""
Advent of Code 2018
Day 6: Chronal Coordinatesw
"""

import click
import os
from pathlib import Path
import regex as re
from collections import defaultdict


def get_points(puzzle_input):
    return [tuple(map(int, re.findall(r'\d+', x))) for x in puzzle_input]


def get_min_max_bounds(points):
    x_min = min(points, key = lambda a: a[0])[0]
    x_max = max(points, key = lambda a: a[0])[0]
    y_min = min(points, key = lambda a: a[1])[1]
    y_max = max(points, key = lambda a: a[1])[1]
    return x_min, x_max, y_min, y_max


def manhattan(p1, p2):
    """
    returns the manhattan distance between p1 and p2
    """
    p1_x, p1_y = p1
    p2_x, p2_y = p2
    return abs(p1_x - p2_x) + abs(p1_y - p2_y)


def distances(p1, points):
    """
    returns the distance from p1 to all points
    """
    d = []
    for i, p2 in enumerate(points):
        dist = manhattan(p1, p2)
        d.append((dist, i))
    return sorted(d)


def solve_part_1(puzzle_input: list[str]):
    points = get_points(puzzle_input)
    x_min, x_max, y_min, y_max = get_min_max_bounds(points)
    closest = defaultdict(int)
    extend_to_inf = set()
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            d = distances((x, y), points)
            if d[0][0] != d[1][0]:
                closest[d[0][1]] += 1
                if x in [x_min, x_max] or y in [y_min, y_max]:  # perimeter
                    extend_to_inf.add(d[0][1])
    for inf in extend_to_inf:
        closest.pop(inf)
    return max(closest.values())


def solve_part_2(puzzle_input: list[str]):
    max_total_distance = int(puzzle_input[0])
    points = get_points(puzzle_input[1:])
    x_min, x_max, y_min, y_max = get_min_max_bounds(points)
    region = set()
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            dists = distances((x, y), points)
            total_d = sum([d[0] for d in dists])
            if total_d < max_total_distance:
                region.add((x, y))
    return len(region)


@click.command()
@click.option("-se", "--skip_example", is_flag=True, default=False)
@click.option("-sp", "--skip_puzzle", is_flag=True, default=False)
def main(skip_example: bool = False, skip_puzzle: bool = False) -> None:
    base_dir = Path(__file__).parent
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
