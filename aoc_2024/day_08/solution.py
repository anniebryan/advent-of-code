"""
Advent of Code 2024
Day 8: Resonant Collinearity
"""

import os
from collections import defaultdict
from pathlib import Path

import click


def parse_input(puzzle_input: list[str]):
    antenna_locs = defaultdict(set)
    for i, row in enumerate(puzzle_input):
        for j, val in enumerate(row):
            if val != ".":
                antenna_locs[val].add((i, j))
    puzzle_size = (len(puzzle_input), len(puzzle_input[0]))
    return antenna_locs, puzzle_size


def in_bounds(antinode_loc, puzzle_size):
    i, j = antinode_loc
    height, width = puzzle_size
    return 0 <= i < height and 0 <= j < width


def get_antinode_locs(antenna_locs, puzzle_size, part_2):
    antinode_locs = set()
    for antennas in antenna_locs.values():
        for antenna_a in antennas:
            for antenna_b in antennas - {antenna_a}:
                diff_i = antenna_a[0] - antenna_b[0]
                diff_j = antenna_a[1] - antenna_b[1]
                if part_2:
                    new_antinode_loc = antenna_a
                    while in_bounds(new_antinode_loc, puzzle_size):
                        antinode_locs.add(new_antinode_loc)
                        new_antinode_loc = (new_antinode_loc[0] + diff_i, new_antinode_loc[1] + diff_j)
                    new_antinode_loc = antenna_b
                    while in_bounds(new_antinode_loc, puzzle_size):
                        antinode_locs.add(new_antinode_loc)
                        new_antinode_loc = (new_antinode_loc[0] - diff_i, new_antinode_loc[1] - diff_j)
                else:
                    antinode_1 = (antenna_a[0] + diff_i, antenna_a[1] + diff_j)
                    antinode_2 = (antenna_b[0] - diff_i, antenna_b[1] - diff_j)
                    if in_bounds(antinode_1, puzzle_size):
                        antinode_locs.add(antinode_1)
                    if in_bounds(antinode_2, puzzle_size):
                        antinode_locs.add(antinode_2)
    return antinode_locs


def solve_part_1(puzzle_input: list[str]):
    antenna_locs, puzzle_size = parse_input(puzzle_input)
    return len(get_antinode_locs(antenna_locs, puzzle_size, False))


def solve_part_2(puzzle_input: list[str]):
    antenna_locs, puzzle_size = parse_input(puzzle_input)
    return len(get_antinode_locs(antenna_locs, puzzle_size, True))


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
