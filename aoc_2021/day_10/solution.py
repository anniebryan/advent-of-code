"""
Advent of Code 2021
Day 10: Syntax Scoring
"""

import click
import os
from pathlib import Path
from collections import deque
from statistics import median

TABLE = {')': 3, ']': 57, '}': 1197, '>': 25137}
POINTS = {')': 1, ']': 2, '}': 3, '>': 4}
OPENING_CHARS = {'(', '[', '{', '<'}
CLOSING_CHARS = {'(': ')', '[': ']', '{': '}', '<': '>'}


def find_first_illegal_char(line):
    chars = deque()
    for s in line:
        if s in OPENING_CHARS:
            chars.append(CLOSING_CHARS[s])
        else:
            expected = chars.pop()
            if s != expected:
                return s


def fill_incomplete(line):
    chars = deque()
    for s in line:
        if s in OPENING_CHARS:
            chars.append(CLOSING_CHARS[s])
        else:
            expected = chars.pop()
            if s != expected:
                return None  # corrupted line
    completion_string = ''
    while chars:
        completion_string += chars.pop()
    return completion_string


def get_score(completion_string):
    score = 0
    for s in completion_string:
        score *= 5
        score += POINTS[s]
    return score


def solve_part_1(puzzle_input: list[str]):
    total = 0
    for line in puzzle_input:
        if (char := find_first_illegal_char(line)) is not None:
            total += TABLE[char]
    return total


def solve_part_2(puzzle_input: list[str]):
    scores = []
    for line in puzzle_input:
        if (completion_string := fill_incomplete(line)) is not None:
            scores.append(get_score(completion_string))
    return median(scores)


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
