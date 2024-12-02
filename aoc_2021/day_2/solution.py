"""
Advent of Code 2021
Day 2: Dive!
"""

import click
import os
import pathlib


def get_commands(puzzle_input):
    return [(n.split(' ')[0], int(n.split(' ')[1])) for n in puzzle_input]


forward = lambda x: x[0] == 'forward'
up = lambda x: x[0] == 'up'
down = lambda x: x[0] == 'down'
amount = lambda x: x[1]


def solve_part_1(puzzle_input: list[str]):
    commands = get_commands(puzzle_input)
    horiz = sum(map(amount, filter(forward, commands)))
    depth = sum(map(amount, filter(down, commands))) - sum(map(amount, filter(up, commands)))
    return horiz * depth


def solve_part_2(puzzle_input: list[str]):
    commands = get_commands(puzzle_input)
    horiz = sum(map(amount, filter(forward, commands)))
    depth, aim = 0, 0
    for x in commands:
        if forward(x):
            depth += aim * amount(x)
        elif down(x):
            aim += amount(x)
        elif up(x):
            aim -= amount(x)
    return horiz * depth


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
