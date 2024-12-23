"""
Advent of Code 2019
Day 1: The Tyranny of the Rocket Equation
"""

import click
import os
import pathlib


def get_masses(puzzle_input):
    masses = [int(m) for m in puzzle_input]
    return masses


def get_fuel(mass: int) -> int:
    """
    :return:
    >>> get_fuel(1969)
    654
    >>> get_fuel(100756)
    33583
    """
    return int(mass / 3) - 2


def get_total_fuel(mass: int) -> int:
    """
    :return:
    >>> get_total_fuel(1969)
    966
    >>> get_total_fuel(100756)
    50346
    """
    initial_fuel = int(mass / 3) - 2
    if initial_fuel <= 0:
        return 0
    return initial_fuel + get_total_fuel(initial_fuel)


def solve_part_1(puzzle_input: list[str]):
    masses = get_masses(puzzle_input)
    return sum([get_fuel(m) for m in masses])


def solve_part_2(puzzle_input: list[str]):
    masses = get_masses(puzzle_input)
    return sum([get_total_fuel(m) for m in masses])


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
