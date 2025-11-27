"""
Advent of Code 2023
Day 12: Hot Springs
"""

import os
from functools import lru_cache
from pathlib import Path

import click


def parse_input(puzzle_input: list[str], part_2: bool) -> list[tuple[str, list[int]]]:
    values = []
    for row in puzzle_input:
        line, criteria = row.split()
        criteria = [int(d) for d in criteria.split(",")]
        if part_2:
            line = f"{line}?{line}?{line}?{line}?{line}"
            criteria = criteria * 5
        values.append((line, criteria))
    return values


@lru_cache(None)
def num_arrangements(line: str, criteria: tuple[int]) -> int:

    if len(line) == 0:
        if len(criteria) == 0:
            return 1
        return 0

    if len(criteria) == 0:
        if "#" in line:
            return 0
        return 1

    if len([ch for ch in line if ch != "."]) < sum(criteria):
        return 0

    if line[0] == ".":
        return num_arrangements(line[1:], criteria)

    if line[0] == "#":
        first_num = criteria[0]
        if len(line) < first_num:
            return 0
        for i in range(first_num):
            if line[i] == ".":
                return 0
        if len(line) > first_num and line[first_num] == "#":
            return 0
        return num_arrangements(line[first_num + 1:], criteria[1:])

    return num_arrangements(f"#{line[1:]}", criteria) + num_arrangements(line[1:], criteria)


def solve_part_1(puzzle_input: list[str]):
    values = parse_input(puzzle_input, False)
    total_num_arrangements = []
    for record, criteria in values:
        n = num_arrangements(record, tuple(criteria))
        total_num_arrangements.append(n)
    return sum(total_num_arrangements)


def solve_part_2(puzzle_input: list[str]):
    values = parse_input(puzzle_input, True)
    total_num_arrangements = []
    for record, criteria in values:
        n = num_arrangements(record, tuple(criteria))
        total_num_arrangements.append(n)
    return sum(total_num_arrangements)


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
