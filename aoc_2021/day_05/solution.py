"""
Advent of Code 2021
Day 5: Hydrothermal Venture
"""

import click
import os
import pathlib
from collections import defaultdict


def get_point_pairs(puzzle_input):
    point_pairs = []
    for line in puzzle_input:
        points = []
        for point in line.split(' -> '):
            points.append(tuple([int(val) for val in point.split(',')]))
        point_pairs.append(tuple(points))
    return point_pairs


def generate_diagram(puzzle_input, diagonals):
    point_pairs = get_point_pairs(puzzle_input)
    diagram = defaultdict(int)
    for point_pair in point_pairs:
        ((x1, y1), (x2, y2)) = point_pair
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        if x1 == x2:  # horizontal
            for y in range(min_y, max_y + 1):
                diagram[(x1, y)] += 1
        elif y1 == y2:  # vertical
            for x in range(min_x, max_x + 1):
                diagram[(x, y1)] += 1
        elif diagonals:  # diagonal
            if (x1 == max_x and y1 == max_y) or (x2 == max_x and y2 == max_y):
                for i in range(max_x - min_x + 1):
                    diagram[(min_x + i, min_y + i)] += 1
            else:
                for i in range(max_x - min_x + 1):
                    diagram[(min_x + i, max_y - i)] += 1
    return diagram


def solve_part_1(puzzle_input: list[str]):
    diagram = generate_diagram(puzzle_input, False)
    return len([key for key in diagram if diagram[key] >= 2])


def solve_part_2(puzzle_input: list[str]):
    diagram = generate_diagram(puzzle_input, True)
    return len([key for key in diagram if diagram[key] >= 2])


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
