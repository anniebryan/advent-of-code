"""
Advent of Code 2020
Day 10: Adapter Array
"""

import os
from collections import defaultdict
from math import prod
from pathlib import Path

import click


def get_numbers(puzzle_input):
    numbers = [int(n) for n in puzzle_input]
    return numbers


def get_differences(numbers):
    numbers = sorted(numbers + [0, max(numbers) + 3])
    d = defaultdict(int)
    for i in range(len(numbers) - 1):
        d[numbers[i + 1] - numbers[i]] += 1
    return d[1], d[3]


def num_arrangements(numbers, last, memo={}):
    n = len(numbers)
    if n in {0, 1}:
        return 1
    if (n, last) not in memo:
        ways = 0
        i = 0
        while i < len(numbers) and numbers[i] <= last + 3:
            ways += num_arrangements(numbers[i + 1:], numbers[i])
            i += 1
        memo[(n, last)] = ways
    return memo[(n, last)]


def solve_part_1(puzzle_input: list[str]):
    numbers = get_numbers(puzzle_input)
    return prod(get_differences(numbers))


def solve_part_2(puzzle_input: list[str]):
    numbers = get_numbers(puzzle_input)
    return num_arrangements(sorted(numbers), 0)


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
