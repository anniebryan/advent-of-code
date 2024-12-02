"""
Advent of Code 2023
Day 5: If You Give A Seed A Fertilizer
"""

import regex as re
from utils import IntRangeSet, IntRangeMap


def get_seeds_to_plant(puzzle_input: list[str], part_2: bool) -> IntRangeSet:
    match = re.match(r'seeds: (?P<seeds>.*)', puzzle_input[0])
    values = [int(d) for d in match.group('seeds').split(" ")]

    seeds_to_plant = IntRangeSet()
    if part_2:
        for i in range(0, len(values), 2):
            seeds_to_plant.add_range(values[i], values[i + 1] - 1)
    else:
        for d in values:
            seeds_to_plant.add_range(d, 0)
    return seeds_to_plant


def create_all_maps(puzzle_input: list[str]) -> None:
    curr_source, curr_dest, curr_map = None, None, None
    for line in puzzle_input[2:]:
        if (match := re.match(r'(?P<source>.*)\-to\-(?P<dest>.*) map:', line)) is not None:
            curr_source = match.group('source')
            curr_dest = match.group('dest')
            curr_map = IntRangeMap(curr_source, curr_dest)
        elif line != "":
            curr_map.add_line_to_map(line)


def map_seed_to_location(seed_range: IntRangeSet) -> IntRangeSet:
    MAP_ORDER = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]
    curr_range = seed_range
    for src, dst in zip(MAP_ORDER[:-1], MAP_ORDER[1:]):
        gardening_map = IntRangeMap.all_maps[(src, dst)]
        curr_range = gardening_map.apply_to_int_range(curr_range)
    return curr_range


def solve_part_1(puzzle_input: list[str]) -> int:
    seeds_to_plant = get_seeds_to_plant(puzzle_input, False)
    create_all_maps(puzzle_input)
    location_range = map_seed_to_location(seeds_to_plant)
    return location_range.min_value


def solve_part_2(puzzle_input: list[str]) -> int:
    seeds_to_plant = get_seeds_to_plant(puzzle_input, True)
    create_all_maps(puzzle_input)
    location_range = map_seed_to_location(seeds_to_plant)
    return location_range.min_value
