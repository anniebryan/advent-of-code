"""
Advent of Code 2024
Day 19: Linen Layout
"""

import os
from pathlib import Path

import click


def parse_input(puzzle_input: list[str]):
    available_patterns = puzzle_input[0].split(", ")
    desired_designs = puzzle_input[2:]
    return available_patterns, desired_designs


def num_ways(design: str, available_patterns: list[str], memo={}) -> int:
    if design in memo:
        return memo[design]

    n = 0
    for p in available_patterns:
        if design == p:
            n += 1
        elif design.startswith(p):
            n += num_ways(design.removeprefix(p), available_patterns, memo)

    memo[design] = n
    return n


def solve_part_1(puzzle_input: list[str]):
    available_patterns, desired_designs = parse_input(puzzle_input)
    return len([d for d in desired_designs if num_ways(d, available_patterns, {}) > 0])


def solve_part_2(puzzle_input: list[str]):
    available_patterns, desired_designs = parse_input(puzzle_input)
    return sum([num_ways(d, available_patterns, {}) for d in desired_designs])


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
