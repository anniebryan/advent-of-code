"""
Advent of Code 2020
Day 20: Jurassic Jigsaw
"""

import os
from collections import deque
from math import prod
from pathlib import Path

import click


def process_input(puzzle_input):
    tiles = {}
    tile_id = None
    tile = []
    for line in puzzle_input:
        if line == "":
            if tile_id is not None:
                tiles[tile_id] = tile
            tile_id = None
            tile = []
        elif tile_id is None:
            tile_id = int(line.split()[1][:-1])
        else:
            tile.append(line)
    if tile_id is not None:
        tiles[tile_id] = tile
    return tiles


def get_edge(tiles, tile, edge):
    """
    tiles:    dictionary mapping tile_id to values
    tile:     tuple of (tile_id, rotation, flipped)
    tile_id:  id indicating tile
    rotation: number of clockwise turns (0, 1, 2, or 3)
    flipped:  True if tile is flipped upside-down
    edge:     which edge to get values of (0, 1, 2, or 3)
    """
    tile_id, rotation, flipped = tile
    values = tiles[tile_id]
    d = (edge - rotation) % 4
    if d == 0:
        if edge in {0, 1}:
            return values[0][::-1] if flipped else values[0]
        if edge in {2, 3}:
            return values[0] if flipped else values[0][::-1]
    elif d == 1:
        i = 0 if flipped else -1
        row = ''.join(r[i] for r in values)
        return row if edge in {0, 1} else row[::-1]
    elif d == 2:
        if edge in {0, 1}:
            return values[-1] if flipped else values[-1][::-1]
        if edge in {2, 3}:
            return values[-1][::-1] if flipped else values[-1]
    else:
        i = -1 if flipped else 0
        row = ''.join(r[i] for r in values)
        return row if edge in {2, 3} else row[::-1]


def match_tile_horizontal(tiles, right_edge, tile_id):
    for rotation in {0, 1, 2, 3}:
        for flipped in {True, False}:
            left_edge = get_edge(tiles, (tile_id, rotation, flipped), 3)
            if left_edge == right_edge:
                yield (rotation, flipped)


def match_tile_vertical(tiles, bottom_edge, tile_id):
    for rotation in {0, 1, 2, 3}:
        for flipped in {True, False}:
            top_edge = get_edge(tiles, (tile_id, rotation, flipped), 0)
            if top_edge == bottom_edge:
                yield (rotation, flipped)


def add_tile(tiles, ids_used, right_edge, bottom_edge):
    for tile_id in tiles:
        if tile_id not in ids_used:
            if right_edge and bottom_edge:
                right_matches = {(r, f) for (r, f) in match_tile_horizontal(tiles, right_edge, tile_id)}
                bottom_matches = {(r, f) for (r, f) in match_tile_vertical(tiles, bottom_edge, tile_id)}
                for (r, f) in right_matches.intersection(bottom_matches):
                    yield (tile_id, r, f)
            elif right_edge:
                for (r, f) in match_tile_horizontal(tiles, right_edge, tile_id):
                    yield (tile_id, r, f)
            elif bottom_edge:
                for (r, f) in match_tile_vertical(tiles, bottom_edge, tile_id):
                    yield (tile_id, r, f)


def build_square(tiles, top_left_tile_id, rotation, flipped):
    square = [(top_left_tile_id, rotation, flipped)]
    width = int(len(tiles) ** 0.5)
    q = deque()
    q.append(square)
    while q:
        square = q.popleft()
        ids_used = set([s[0] for s in square])
        if len(square) == len(tiles):
            return square

        right_edge = get_edge(tiles, square[-1], 1) if len(square) % width != 0 else None
        bottom_edge = get_edge(tiles, square[len(square) - width], 2) if len(square) >= width else None

        for tile in add_tile(tiles, ids_used, right_edge, bottom_edge):
            q.append(square + [tile])
    return None


def find_top_left_tile(tiles):
    for tile_id in tiles:
        for rotation in {0, 1, 2, 3}:
            for flipped in {True, False}:
                square = build_square(tiles, tile_id, rotation, flipped)
                if square is not None:
                    return square
    return None


def get_corners(tiles):
    square = find_top_left_tile(tiles)
    width = int(len(tiles) ** 0.5)
    return {square[0][0], square[width-1][0], square[len(square)-width][0], square[-1][0]}


def remove_border(tiles, tile):
    tile_id = tile[0]
    values = tiles[tile_id]
    return [row[1:-1] for row in values[1:-1]]


def get_tile_image(tiles, tile, borderless):
    tile_id, rotation, flipped = tile
    tile_image = remove_border(tiles, tile) if borderless else tiles[tile_id]
    width = len(tile_image)

    if flipped:
        tile_image = [row[::-1] for row in tile_image]

    if rotation == 0:
        return tile_image
    elif rotation == 1:
        return [''.join(tile_image[width - j - 1][i] for j in range(width)) for i in range(width)]
    elif rotation == 2:
        return [row[::-1] for row in tile_image[::-1]]
    else:
        return [''.join(tile_image[j][width - i - 1] for j in range(width)) for i in range(width)]


def get_image(tiles):
    square = find_top_left_tile(tiles)
    width = int(len(tiles) ** 0.5)
    image = []
    for i in range(width):
        image_row = [get_tile_image(tiles, square[width * i + j], True) for j in range(width)]
        for k in range(len(image_row[0])):
            image.append(''.join(col[k] for col in image_row))
    return image


def get_squares(tiles, char):
    image = get_image(tiles)
    for i, row in enumerate(image):
        for j, c in enumerate(row):
            if c == char:
                yield (i, j)


def get_pattern(rotation, flipped, pattern):
    if flipped:
        pattern = {(18 - i, j) for (i, j) in pattern}
    if rotation == 1:
        pattern = {(j, 2 - i) for (i, j) in pattern}
    elif rotation == 2:
        pattern = {(2 - i, 18 - j) for (i, j) in pattern}
    elif rotation == 3:
        pattern = {(j, i) for (i, j) in pattern}
    return pattern


def fits_pattern(tiles, image, char, rotation, flipped, pattern):
    dim = (2, 18) if rotation % 2 == 0 else (18, 2)
    pattern = get_pattern(rotation, flipped, pattern)

    locs = set(get_squares(tiles, char))
    num_pattern_matches = 0

    width = len(image)
    for x in range(width-dim[0]):
        for y in range(width-dim[1]):
            if all([(x + i, y + j) in locs for (i, j) in pattern]):
                num_pattern_matches += 1
    return num_pattern_matches


def num_char_not_in_pattern(tiles, char, pattern):
    image = get_image(tiles)
    max_matches = 0
    for rotation in {0, 1, 2, 3}:
        for flipped in {True, False}:
            max_matches = max(fits_pattern(tiles, image, char, rotation, flipped, pattern), max_matches)
    return len(set(get_squares(tiles, char))) - len(pattern) * max_matches


def solve_part_1(puzzle_input: list[str]):
    tiles = process_input(puzzle_input)
    corners = list(get_corners(tiles))
    return f"{corners[0]} * {corners[1]} * {corners[2]} * {corners[3]} = {prod(corners)}"


def solve_part_2(puzzle_input: list[str]):
    tiles = process_input(puzzle_input)
    pattern = {
        (0, 18), (1, 0), (1, 5), (1, 6), (1, 11), (1, 12), (1, 17), (1, 18), (1, 19),\
        (2, 1), (2, 4), (2, 7), (2, 10), (2, 13), (2, 16),
    }
    return num_char_not_in_pattern(tiles, '#', pattern)
