"""
Advent of Code 2023
Day 5: If You Give A Seed A Fertilizer
"""

import click
import os
import pathlib
import regex as re
from utils import IntRangeSet, IntRangeMap


def parse_input(puzzle_input: list[str], part_2: bool) -> tuple[IntRangeSet, dict[tuple[str, str], IntRangeMap]]:

    seed_values = list(int(t) for t in puzzle_input[0].strip().split()[1:])
    seeds = IntRangeSet()
    if part_2:
        for i in range(0, len(seed_values), 2):
            seeds.add_range(seed_values[i], seed_values[i + 1] - 1)
    else:
        for d in seed_values:
            seeds.add_value(d)

    all_maps = {}
    source_type, dest_type, curr_map = None, None, None
    for line in puzzle_input[2:]:
        if (match := re.match(r'(?P<source>.*)\-to\-(?P<dest>.*) map:', line)) is not None:
            source_type = match.group('source')
            dest_type = match.group('dest')
            curr_map = IntRangeMap(source_type, dest_type)
        elif line != "":
            curr_map.add_line_to_map(line)
        all_maps[(source_type, dest_type)] = curr_map

    return seeds, all_maps


def map_seed_to_location(seed_range: IntRangeSet, all_maps: dict[tuple[str, str], IntRangeMap]) -> IntRangeSet:
    MAP_ORDER = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]
    curr_range = seed_range
    for src, dst in zip(MAP_ORDER[:-1], MAP_ORDER[1:]):
        gardening_map = all_maps[(src, dst)]
        curr_range = gardening_map.apply_to_int_range(curr_range)
    return curr_range


def solve_part_1(puzzle_input: list[str]) -> int:
    seeds_to_plant, all_maps = parse_input(puzzle_input, False)
    location_range = map_seed_to_location(seeds_to_plant, all_maps)
    return location_range.min_value


def solve_part_2(puzzle_input: list[str]) -> int:
    seeds_to_plant, all_maps = parse_input(puzzle_input, True)
    location_range = map_seed_to_location(seeds_to_plant, all_maps)
    return location_range.min_value


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
