"""
Advent of Code 2024
Day 11: Plutonian Pebbles
"""

import click
import os
import pathlib


def parse_input(puzzle_input: list[str]):
    return [int(n) for n in puzzle_input[0].split()]


def get_num_stones(val: int, num_blinks: int, memo) -> int:
    if (val, num_blinks) in memo:
        return memo[(val, num_blinks)]

    if num_blinks == 0:
        memo[(val, num_blinks)] = 1
        return 1

    if val == 0:
        memo[(val, num_blinks)] = get_num_stones(1, num_blinks - 1, memo)
        return memo[(val, num_blinks)]

    if (l := len(str(val))) % 2 == 0:
        m = int(l / 2)
        left = get_num_stones(int(str(val)[:m]), num_blinks - 1, memo)
        right = get_num_stones(int(str(val)[m:]), num_blinks - 1, memo)
        memo[(val, num_blinks)] = left + right
        return memo[(val, num_blinks)]

    memo[(val, num_blinks)] = get_num_stones(val * 2024, num_blinks - 1, memo)
    return memo[(val, num_blinks)]


def solve(vals: list[int], num_blinks: int) -> int:
    tot_stones = 0
    memo = {}
    for val in vals:
        tot_stones += get_num_stones(val, num_blinks, memo)
    return tot_stones


def solve_part_1(puzzle_input: list[str]):
    vals = parse_input(puzzle_input)
    return solve(vals, 25)


def solve_part_2(puzzle_input: list[str]):
    vals = parse_input(puzzle_input)
    return solve(vals, 75)


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
