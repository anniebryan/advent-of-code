"""
Advent of Code 2021
Day 7: The Threachery of Whales
"""

import click
import os
import pathlib


def get_positions(puzzle_input):
    return [int(val) for val in puzzle_input[0].split(',')]


def min_distance(puzzle_input, distance_fn):
    positions = get_positions(puzzle_input)
    return min([distance_fn(i, positions) for i in range(max(positions))])


def solve_part_1(puzzle_input: list[str]):
    abs_distance = lambda i, positions: int(sum([abs(p - i) for p in positions]))
    return min_distance(puzzle_input, abs_distance)


def solve_part_2(puzzle_input: list[str]):
    distance = lambda i, positions: int(sum([abs(p - i) * (abs(p - i) + 1) / 2 for p in positions]))
    return min_distance(puzzle_input, distance)


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
