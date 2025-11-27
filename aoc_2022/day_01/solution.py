"""
Advent of Code 2022
Day 1: Calorie Counting
"""

import click
import os
import pathlib


def get_max_three(a, b, c, current_elf):
    if current_elf > c:
        c = current_elf
        if current_elf > b:
            b, c = current_elf, b
            if current_elf > a:
                a, b = current_elf, a
    return a, b, c


def max_three_elves(puzzle_input):
    a, b, c = 0, 0, 0
    current_elf = 0
    for cal in puzzle_input:
        if cal == '':
            a, b, c = get_max_three(a, b, c, current_elf)
            current_elf = 0
        else:
            current_elf += int(cal)
    return get_max_three(a, b, c, current_elf)


def solve_part_1(puzzle_input: list[str]):
    return max_three_elves(puzzle_input)[0]


def solve_part_2(puzzle_input: list[str]):
    return sum(max_three_elves(puzzle_input))


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
