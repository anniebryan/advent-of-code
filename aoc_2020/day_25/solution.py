"""
Advent of Code 2020
Day 25: Combo Breaker
"""

import click
import os
from pathlib import Path


def get_public_keys(puzzle_input):
    return [int(key) for key in puzzle_input]


def get_loop_size(keys, subject_number, upper_bound):
    for i, val in transform(subject_number, upper_bound):
        if val in keys:
            return i, val


def transform(subject_number, loop_size):
    val = 1
    for i in range(loop_size):
        val *= subject_number
        val %= 20201227
        yield i + 1, val


def other_key(keys, key):
    if key == keys[0]:
        return keys[1]
    return keys[0]


def solve_part_1(puzzle_input: list[str]):
    keys = get_public_keys(puzzle_input)
    loop_size, key = get_loop_size(keys, 7, 10000000)
    return list(transform(other_key(keys, key), loop_size))[-1][1]


def solve_part_2(puzzle_input: list[str]):
    return


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
