"""
Advent of Code 2024
Day 1: Historian Hysteria
"""

import click
import os
import pathlib
import regex as re
from collections import Counter

def parse_input(puzzle_input):
    left_list, right_list = [], []
    for line in puzzle_input:
        nums = re.findall('\d+', line)
        assert len(nums) == 2
        left_num, right_num = nums
        left_list.append(int(left_num))
        right_list.append(int(right_num))
    return sorted(left_list), sorted(right_list)


def solve_part_1(puzzle_input):
    left_list, right_list = parse_input(puzzle_input)
    all_distances = []
    for x, y in zip(left_list, right_list):
        all_distances.append(abs(x - y))
    return sum(all_distances)


def solve_part_2(puzzle_input):
    left_list, right_list = parse_input(puzzle_input)
    right_occurrences = Counter(right_list)
    all_distances = []
    for x in left_list:
        all_distances.append(x * right_occurrences[x])
    return sum(all_distances)


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
