"""
Advent of Code 2022
Day 6: Tuning Trouble
"""

import click
import os
from pathlib import Path


def all_different(last_elems):
    return len(last_elems) == len(set(last_elems))


def find_marker(puzzle_input, n):
    puzzle_input = puzzle_input[0]
    last_n = tuple(puzzle_input[:n])
    for i, ch in enumerate(puzzle_input[n:]):
        if all_different(last_n):
            return i + n
        else:
            last_n = last_n[1:] + (ch,)


def solve_part_1(puzzle_input: list[str]):
    return find_marker(puzzle_input, 4)


def solve_part_2(puzzle_input: list[str]):
    return find_marker(puzzle_input, 14)


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
