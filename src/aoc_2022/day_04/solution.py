"""
Advent of Code 2022
Day 4: Camp Cleanup
"""

import os
from pathlib import Path

import click


def get_sections(puzzle_input):
    for r in puzzle_input:
        elf_one, elf_two = r.split(',')
        a, b = elf_one.split('-')
        c, d = elf_two.split('-')
        yield int(a), int(b), int(c), int(d)


def solve_part_1(puzzle_input: list[str]):
    num_overlap = 0
    for a, b, c, d in get_sections(puzzle_input):
        if a <= c <= d <= b:
            num_overlap += 1
        elif c <= a <= b <= d:
            num_overlap += 1
    return num_overlap


def solve_part_2(puzzle_input: list[str]):
    num_overlap = 0
    for a, b, c, d in get_sections(puzzle_input):
        if a <= c <= b:
            num_overlap += 1
        elif c <= a <= d:
            num_overlap += 1
    return num_overlap


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
