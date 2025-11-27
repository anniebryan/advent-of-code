"""
Advent of Code 2020
Day 13: Shuttle Search
"""

import os
from math import prod
from pathlib import Path

import click


def get_earliest_bus(puzzle_input):
    return int(puzzle_input[0])


def get_bus_times(puzzle_input):
    times = puzzle_input[1].split(',')
    return {int(x) for x in times if x != 'x'}


def next_bus_time(puzzle_input):
    earliest_bus = get_earliest_bus(puzzle_input)
    bus_times = get_bus_times(puzzle_input)
    time_to_wait = {x: x - earliest_bus % x for x in bus_times}
    min_time = min(time_to_wait.values())
    for k, v in time_to_wait.items():
        if v == min_time:
            return k, min_time


def get_departure_requirements(puzzle_input):
    times = puzzle_input[1].split(',')
    return {(i, int(times[i])) for i in range(len(times)) if times[i] != 'x'}


def get_earliest_timestamp(puzzle_input):
    requirements = get_departure_requirements(puzzle_input)
    offsets = {(b - a % b, b) for a,b in requirements}
    time, inc = 0, 1
    for t, bus in offsets:
        while time % bus != t % bus:
            time += inc
        inc *= bus
    return time


def solve_part_1(puzzle_input: list[str]):
    return prod(next_bus_time(puzzle_input))


def solve_part_2(puzzle_input: list[str]):
    return get_earliest_timestamp(puzzle_input)


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
