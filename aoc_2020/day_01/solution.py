"""
Advent of Code 2020
Day 1: Report Repair
"""

import click
import os
import pathlib
from collections import defaultdict
from math import prod


def get_expense_report(puzzle_input):
    expense_report = [int(i) for i in puzzle_input]
    return expense_report


def find_two_that_sum(expense_report, n):
    seen = set()
    for i in expense_report:
        if n - i in seen:
            return (i, n - i)
        else:
            seen.add(i)
    return (0, 0)  # no two entries sum to n


def find_three_that_sum(expense_report, n):
    two_way_sums = set()
    two_way_map = defaultdict(set)  # maps sum to set of tuples of indices
    for i in range(len(expense_report)):
        for j in range(i, len(expense_report)):
            s = expense_report[i] + expense_report[j]
            two_way_sums.add(s)
            two_way_map[s].add((i, j))
    for k in range(len(expense_report)):
        missing = n - expense_report[k]
        if missing in two_way_sums:
            for tup in two_way_map[missing]:
                if k not in tup:
                    (i, j) = tup
                    return (expense_report[i], expense_report[j], expense_report[k])
    return (0, 0, 0)  # no three entries sum to n


def solve_part_1(puzzle_input: list[str]):
    expense_report = get_expense_report(puzzle_input)
    return prod(find_two_that_sum(expense_report, 2020))


def solve_part_2(puzzle_input: list[str]):
    expense_report = get_expense_report(puzzle_input)
    return prod(find_three_that_sum(expense_report, 2020))


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
