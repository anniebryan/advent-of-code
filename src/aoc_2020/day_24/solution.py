"""
Advent of Code 2020
Day 24: Lobby Layout
"""

from collections import defaultdict


def get_instructions(puzzle_input):
    instructions = []
    for line in puzzle_input:
        instruction = []
        i = 0
        while i < len(line):
            if line[i] in {'n', 's'}:
                instruction.append(line[i:i + 2])
                i += 2
            else:
                instruction.append(line[i])
                i += 1
        instructions.append(instruction)
    return instructions


def flip_tile(instruction):
    i, j = 0, 0
    for step in instruction:
        if step == 'e':
            i += 1
        elif step == 'w':
            i -= 1
        elif step in {'ne', 'se'}:
            i += 0.5
        elif step in {'nw', 'sw'}:
            i -= 0.5

        if step in {'nw', 'ne'}:
            j += 1
        elif step in {'sw', 'se'}:
            j -= 1
    return i, j


def process_all_instructions(puzzle_input):
    instructions = get_instructions(puzzle_input)
    flipped_tiles = defaultdict(int)
    for instruction in instructions:
        i, j = flip_tile(instruction)
        flipped_tiles[(i, j)] += 1
    return flipped_tiles


def get_black_tiles(flipped_tiles):
    return {tile for tile in flipped_tiles if flipped_tiles[tile] % 2 == 1}


def get_num_black_tiles(puzzle_input):
    flipped_tiles = process_all_instructions(puzzle_input)
    return len(get_black_tiles(flipped_tiles))


def get_adjacent_tiles(tile):
    i, j = tile
    return {(i + 1, j), (i + 0.5, j + 1), (i + 0.5, j - 1), (i - 1, j), (i - 0.5, j + 1), (i - 0.5, j - 1)}


def num_black_adjacent_tiles(tile, black_tiles):
    adjacent_tiles = get_adjacent_tiles(tile)
    return len([t for t in adjacent_tiles if t in black_tiles])


def get_white_tiles(black_tiles):
    all_adjacent = set()
    for black_tile in black_tiles:
        adjacent = get_adjacent_tiles(black_tile)
        all_adjacent |= adjacent
    return all_adjacent.difference(black_tiles)


def wait_day(black_tiles):
    tiles_to_flip = set()
    for black_tile in black_tiles:
        num = num_black_adjacent_tiles(black_tile, black_tiles)
        if num == 0 or num > 2:
            tiles_to_flip.add(black_tile)
    for white_tile in get_white_tiles(black_tiles):
        num = num_black_adjacent_tiles(white_tile, black_tiles)
        if num == 2:
            tiles_to_flip.add(white_tile)
    return tiles_to_flip


def wait_n_days(puzzle_input, n):
    flipped_tiles = process_all_instructions(puzzle_input)
    black_tiles = get_black_tiles(flipped_tiles)
    for _ in range(n):
        tiles_to_flip = wait_day(black_tiles)
        for tile in tiles_to_flip:
            flipped_tiles[tile] += 1
        black_tiles = get_black_tiles(flipped_tiles)
    return len(black_tiles)


def solve_part_1(puzzle_input: list[str]):
    return get_num_black_tiles(puzzle_input)


def solve_part_2(puzzle_input: list[str]):
    return wait_n_days(puzzle_input, 100)
