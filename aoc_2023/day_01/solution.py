"""
Advent of Code 2023
Day 1: Trebuchet?!
"""

import click
import os
from pathlib import Path

DIGIT_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}


def map_index_to_digit(line: str, part_2: bool) -> dict[int, int]:
    digit_map = {}
    for i, char in enumerate(line):
        if char.isdigit():
            digit_map[i] = int(char)
    if part_2:
        for k, v in DIGIT_WORDS.items():
            for i in range(len(line) - len(k) + 1):
                if line[i:i + len(k)] == k:
                    digit_map[i] = v
    return digit_map


def get_calibration_value(line: str, part_2: bool) -> int:
    digit_map = map_index_to_digit(line, part_2)
    min_ix, max_ix = min(digit_map), max(digit_map)
    first_digit, last_digit = digit_map[min_ix], digit_map[max_ix]
    return int(f"{first_digit}{last_digit}")


def get_all_calibration_values(puzzle_input: list[str], part_2: bool) -> list[int]:
    calibration_values = []
    for line in puzzle_input:
        calibration_values.append(get_calibration_value(line, part_2))
    return calibration_values


def solve_part_1(puzzle_input: list[str]) -> int:
    if puzzle_input[0] == "part 2 only":
        return "Not supported"
    return sum(get_all_calibration_values(puzzle_input[1:], False))


def solve_part_2(puzzle_input: list[str]) -> int:
    if puzzle_input[0] == "part 1 only":
        return "Not supported"
    return sum(get_all_calibration_values(puzzle_input[1:], True))


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
