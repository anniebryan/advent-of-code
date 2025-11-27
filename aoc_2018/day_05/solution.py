"""
Advent of Code 2018
Day 5: Alchemical Reduction
"""

import click
import os
import pathlib
import string
from functools import reduce


def destroy(p, c):
    # p: previous
    # c: current
    if p is None or len(p) == 0:
        return c
    else:
        l = str(p[-1:])  # last letter
        lc = string.ascii_lowercase
        uc = string.ascii_uppercase
        if (l in lc and c in uc) or (l in uc and c in lc):  # opposite case
            if l.lower() == c.lower():
                return p[:-1]
        return p + c


def solve_part_1(puzzle_input: list[str]):
    s = puzzle_input[0]
    s2 = reduce(destroy, s)
    return len(s2)


def solve_part_2(puzzle_input: list[str]):
    s = puzzle_input[0]
    lengths = {}
    for letter in string.ascii_lowercase:
        s_ = s[:]  # copies to avoid mutating
        s_ = s.replace(letter, '').replace(letter.upper(), '')
        s_ = reduce(destroy, s_)
        lengths[len(s_)] = letter
    num = min(lengths.keys())
    return f"Removing the letter {lengths[num]} yields a string of length {num}"


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
