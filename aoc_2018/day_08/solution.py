"""
Advent of Code 2018
Day 8: Memory Maneuver
"""

import click
import os
from pathlib import Path
import regex as re


def process_data(data):
    num_children = next(data)
    num_metadata = next(data)
    children = [process_data(data) for _ in range(num_children)]
    metadata = [next(data) for _ in range(num_metadata)]
    return children, metadata


def solve_part_1(puzzle_input: list[str]):
    # returns sum of metadata values for all nodes
    def sum_metadata(node):
        children, metadata = node
        return sum(metadata) + sum(sum_metadata(child) for child in children)

    data = (int(d) for d in re.findall(r'\d+', puzzle_input[0]))
    root = process_data(data)
    return sum_metadata(root)


def solve_part_2(puzzle_input: list[str]):
    # returns value of root node
    def value(node):
        children, metadata = node
        if not children:
            return sum(metadata)
        else:
            return sum([value(children[m - 1]) for m in metadata if m <= len(children)])

    data = (int(d) for d in re.findall(r'\d+', puzzle_input[0]))
    root = process_data(data)
    return value(root)


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
