"""
Advent of Code 2023
Day 6: Wait For It
"""

import os
from math import prod
from pathlib import Path

import click


def parse_input(puzzle_input: list[str], part_2: bool):
    if part_2:
        times = [int("".join(puzzle_input[0].split()[1:]))]
        dists = [int("".join(puzzle_input[1].split()[1:]))]
    else:
        times = [int(d) for d in puzzle_input[0].split()[1:]]
        dists = [int(d) for d in puzzle_input[1].split()[1:]]
    return list(zip(times, dists))


def num_ways_to_win(time, dist_record):
    num_ways = 0
    for num_ms in range(time + 1):
        distance_traveled = num_ms * (time - num_ms)
        if distance_traveled > dist_record:
            num_ways += 1
    return num_ways


def solve_part_1(puzzle_input: list[str]):
    races = parse_input(puzzle_input, False)
    all_num_ways = []
    for time, dist_record in races:
        all_num_ways.append(num_ways_to_win(time, dist_record))
    return prod(all_num_ways)


def solve_part_2(puzzle_input: list[str]):
    time, dist_record = parse_input(puzzle_input, True)[0]
    return num_ways_to_win(time, dist_record)


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
