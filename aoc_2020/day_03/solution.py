"""
Advent of Code 2020
Day 3: Toboggan Trajectory
"""

import os
from math import prod
from pathlib import Path

import click


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
