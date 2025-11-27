"""
Advent of Code 2022
Day 3: Rucksack Reorganization
"""

import click
import os
from pathlib import Path


def letter_in_common(row):
    n = len(row) // 2
    left = set()
    for i in range(len(row)):
        ch = row[i]
        if i < n:
            left.add(ch)
        elif ch in left:
            return ch


def letter_in_common_3(a, b, c):
    a_ch = set([ch for ch in a])
    b_ch = set([ch for ch in b])
    for ch in c:
        if ch in a_ch and ch in b_ch:
            return ch


def priority(ch):
    if 97 <= ord(ch) <= 122:
        return ord(ch) - 96
    return ord(ch) - 38


def solve_part_1(puzzle_input: list[str]):
    tot = 0
    for row in puzzle_input:
        ch = letter_in_common(row)
        tot += priority(ch)
    return tot


def solve_part_2(puzzle_input: list[str]):
    tot = 0
    for i in range(0, len(puzzle_input), 3):
        ch = letter_in_common_3(*puzzle_input[i:i + 3])
        tot += priority(ch)
    return tot


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
