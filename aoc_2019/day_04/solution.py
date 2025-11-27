"""
Advent of Code 2019
Day 4: Secure Container
"""

import os
from pathlib import Path

import click
import regex as re


def get_min_max_r(puzzle_input):
    min_r, max_r = (int(x) for x in re.findall(r"(\d+)-(\d+)", puzzle_input[0])[0])
    return min_r, max_r


def adjacent_digits(n):
    s = str(n)
    adjacent = [s[i] == s[i + 1] for i in range(len(s) - 1)]
    return any(adjacent)


def never_decreases(n):
    s = str(n)
    decreases = [s[i] > s[i + 1] for i in range(len(s) - 1)]
    return not any(decreases)


def contains_double(n):
    s = str(n)
    lengths = []
    current = 1
    for i in range(len(s) - 1):
        if s[i] == s[i + 1]:
            current += 1
        else:
            lengths.append(current)
            current = 1
    lengths.append(current)
    return 2 in lengths


def solve_part_1(puzzle_input: list[str]):
    min_r, max_r = get_min_max_r(puzzle_input)
    valid_passwords = [n for n in range(min_r, max_r + 1) if adjacent_digits(n) and never_decreases(n)]
    return len(valid_passwords)


def solve_part_2(puzzle_input: list[str]):
    min_r, max_r = get_min_max_r(puzzle_input)
    valid_passwords = [n for n in range(min_r, max_r + 1) if contains_double(n) and never_decreases(n)]
    return len(valid_passwords)


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
