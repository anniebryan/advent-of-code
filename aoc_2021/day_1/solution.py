"""
Advent of Code 2021
Day 1: Sonar Sweep
"""

import click
import os
import pathlib


def increasing(x, y):
	return y > x


def three_sum(x, y, z):
	return x + y + z


def solve_part_1(puzzle_input: list[str]):
	measurements = get_measurements(puzzle_input)
	return sum(map(increasing, measurements, measurements[1:]))


def solve_part_2(puzzle_input: list[str]):
	measurements = get_measurements(puzzle_input)
	sums = list(map(three_sum, measurements, measurements[1:], measurements[2:]))
	return sum(map(increasing, sums, sums[1:]))


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
