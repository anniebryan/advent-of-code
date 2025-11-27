"""
Advent of Code 2018
Day 2: Inventory Management System
"""

import os
import string
from pathlib import Path

import click


def solve_part_1(puzzle_input: list[str]):
    num_2, num_3 = 0, 0
    for box in puzzle_input:
        counts = []
        for letter in string.ascii_lowercase:
            count = box.count(letter)
            counts.append(count)
        if 2 in counts:
            num_2 += 1
        if 3 in counts:
            num_3 += 1
    return num_2 * num_3


def solve_part_2(puzzle_input: list[str]):
    for i in range(len(puzzle_input)):
        box_1 = puzzle_input[i]
        remaining = puzzle_input[i + 1:]
        for j in range(len(remaining)):
            box_2 = remaining[j]
            different = 0
            for l in range(len(box_1) - 1):  # all 27 letters
                if box_1[l] != box_2[l]:
                    different += 1
                    letter = l
            if different == 1:
                return box_1[0:letter] + box_1[letter + 1:]


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
