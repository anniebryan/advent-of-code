"""
Advent of Code 2020
Day 6: Custom Customs
"""

import click
import os
import pathlib
from collections import defaultdict


def get_all_groups(puzzle_input):
    all_groups = []
    group = []
    for line in puzzle_input:
        if line == "":
            # break between groups
            all_groups.append(group)
            group = []
        else:
            # continuation of current group
            group.extend(line.split())
    all_groups.append(group)
    return all_groups


def get_questions_at_least_one_yes(group):
    return {char for person in group for char in person}


def get_questions_all_yes(group):
    d = defaultdict(int)
    for person in group:
        for char in person:
            d[char] += 1
    return {key for key in d if d[key] == len(group)}


def get_sum_counts(puzzle_input, fn):
    return sum([len(fn(group)) for group in get_all_groups(puzzle_input)])


def solve_part_1(puzzle_input: list[str]):
    return get_sum_counts(puzzle_input, get_questions_at_least_one_yes)


def solve_part_2(puzzle_input: list[str]):
    return get_sum_counts(puzzle_input, get_questions_all_yes)


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
