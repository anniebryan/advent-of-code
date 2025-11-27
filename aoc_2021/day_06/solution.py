"""
Advent of Code 2021
Day 6: Lanternfish
"""

import os
from collections import defaultdict
from pathlib import Path

import click


def get_initial_timers(puzzle_input):
    timers = defaultdict(int)
    for val in puzzle_input[0].split(','):
        timers[int(val)] += 1
    return timers


def simulate_day(timers):
    new_timers = {key - 1: val for key, val in timers.items() if key != 0}
    if 0 in timers:
        new_timers[6] = new_timers[6] + timers[0] if 6 in new_timers else timers[0]
        new_timers[8] = new_timers[8] + timers[0] if 8 in new_timers else timers[0]
    return new_timers


def simulate_n_days(puzzle_input, n):
    timers = get_initial_timers(puzzle_input)
    for _ in range(n):
        timers = simulate_day(timers)
    return timers


def solve_part_1(puzzle_input: list[str]):
    return sum(simulate_n_days(puzzle_input, 80).values())


def solve_part_2(puzzle_input: list[str]):
    return sum(simulate_n_days(puzzle_input, 256).values())


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
