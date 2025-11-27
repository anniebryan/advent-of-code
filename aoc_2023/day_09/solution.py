"""
Advent of Code 2023
Day 9: Mirage Maintenance
"""

import click
import os
from pathlib import Path


def parse_input(puzzle_input: list[str]):
    return [[int(n) for n in line.split()] for line in puzzle_input]


def predict_next_value(seq: list[int]) -> int:
    diffs = [b - a for a, b in zip(seq, seq[1:])]
    if set(diffs) == {0}:
        return seq[-1]
    return seq[-1] + predict_next_value(diffs)


def predict_first_value(seq: list[int]) -> int:
    diffs = [b - a for a, b in zip(seq, seq[1:])]
    if set(diffs) == {0}:
        return seq[0]
    return seq[0] - predict_first_value(diffs)


def solve_part_1(puzzle_input: list[str]):
    sequences = parse_input(puzzle_input)
    next_values = []
    for seq in sequences:
        next_values.append(predict_next_value(seq))
    return sum(next_values)


def solve_part_2(puzzle_input: list[str]):
    sequences = parse_input(puzzle_input)
    first_values = []
    for seq in sequences:
        first_values.append(predict_first_value(seq))
    return sum(first_values)


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
