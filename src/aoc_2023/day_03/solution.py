"""
Advent of Code 2023
Day 3: Gear Ratios
"""

import os
from math import prod
from pathlib import Path

import click

ADJACENT_OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def get_symbol_locations(puzzle_input: list[str], gear_symbol: str = None) -> set[tuple[int, int]]:
    def include(char: str) -> bool:
        if gear_symbol is None:
            return char != "." and not char.isdigit()
        else:
            return char == gear_symbol

    all_symbol_locations = set()
    for i, row in enumerate(puzzle_input):
        for j, char in enumerate(row):
            if include(char):
                all_symbol_locations.add((i, j))
    return all_symbol_locations


def get_number_map(puzzle_input: list[str]) -> tuple[dict[tuple[int, int], int], dict[int, int]]:
    num_id = 0
    loc_to_num_id_map = {}
    num_id_map = {}
    for i, row in enumerate(puzzle_input):
        j = 0
        while j < len(row):
            char = row[j]
            k = 1
            if char.isdigit():
                while j + k < len(row) and row[j + k].isdigit():
                    k += 1
                num = int(row[j:j + k])
                num_id_map[num_id] = num
                for l in range(j, j + k):
                    loc_to_num_id_map[(i, l)] = num_id
                num_id += 1
            j += k
    return loc_to_num_id_map, num_id_map


def get_adjacent_locs(loc: tuple[int, int]) -> set[tuple[int, int]]:
    i, j = loc
    return {(i + di, j + dj) for di, dj in ADJACENT_OFFSETS}


def get_adjacent_num_ids(loc_to_num_id_map: dict[tuple[int, int], int], loc: tuple[int, int]) -> set[int]:
    adjacent_num_ids = set()
    for adj_loc in get_adjacent_locs(loc):
        if adj_loc in loc_to_num_id_map:
            adjacent_num_ids.add(loc_to_num_id_map[adj_loc])
    return adjacent_num_ids


def get_adjacent_numbers(adjacent_num_ids: set[int], num_id_map: dict[int, int]) -> list[int]:
    adjacent_numbers = []
    for num_id in adjacent_num_ids:
        adjacent_numbers.append(num_id_map[num_id])
    return adjacent_numbers


def solve_part_1(puzzle_input: list[str]) -> int:
    loc_to_num_id_map, num_id_map = get_number_map(puzzle_input)

    all_adjacent_num_ids = set()
    for loc in get_symbol_locations(puzzle_input):
        all_adjacent_num_ids |= get_adjacent_num_ids(loc_to_num_id_map, loc)

    adjacent_numbers = get_adjacent_numbers(all_adjacent_num_ids, num_id_map)
    return sum(adjacent_numbers)
            

def solve_part_2(puzzle_input: list[str]) -> int:
    loc_to_num_id_map, num_id_map = get_number_map(puzzle_input)

    all_gear_ratios = []
    for gear_symbol_loc in get_symbol_locations(puzzle_input, "*"):
        adjacent_num_ids = get_adjacent_num_ids(loc_to_num_id_map, gear_symbol_loc)
        if len(adjacent_num_ids) == 2:
            adjacent_numbers = get_adjacent_numbers(adjacent_num_ids, num_id_map)
            all_gear_ratios.append(prod(adjacent_numbers))
    return sum(all_gear_ratios)
