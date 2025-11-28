"""
Advent of Code 2023
Day 16: The Floor Will Be Lava
"""

from collections import deque
from typing import Iterator

from utils import Grid


def move_beam(g: Grid, start_pos: tuple[int, int], start_direction: tuple[int, int]) -> Iterator[tuple[int, int]]:
    q = deque([(start_pos, start_direction)])
    seen_pos_direction = set()
    visited_locs = set()
    while q:
        pos, direction = q.pop()
        if (pos, direction) not in seen_pos_direction:
            seen_pos_direction.add((pos, direction))
            x, y = pos
            if g.in_bounds(x, y):
                visited_locs.add(pos)
                val = g.at(x, y)
                dx, dy = direction
                if val == ".":
                    q.append(((x + dx, y + dy), direction))
                elif val == "/":
                    q.append(((x - dy, y - dx), (-dy, -dx)))
                elif val == "\\":
                    q.append(((x + dy, y + dx), (dy, dx)))
                elif val == "|":
                    if dy == 0:
                        q.append(((x + dx, y + dy), direction))
                    else:
                        q.append(((x + 1, y), (1, 0)))
                        q.append(((x - 1, y), (-1, 0)))
                elif val == "-":
                    if dx == 0:
                        q.append(((x + dx, y + dy), direction))
                    else:
                        q.append(((x, y + 1), (0, 1)))
                        q.append(((x, y - 1), (0, -1)))
                else:
                    raise ValueError(f"Unexpected {pos=} {val=}")
    return visited_locs


def calc_num_energized(g, start_pos, start_dir) -> int:
    energized_tiles = set()
    for tile in move_beam(g, start_pos, start_dir):
        energized_tiles.add(tile)
    return len(energized_tiles)


def all_possible_start_configs(g: Grid) -> Iterator[tuple[tuple[int, int], tuple[int, int]]]:
    # 4 corners
    for (x, dx) in [(0, 1), (g.height - 1, -1)]:
        for (y, dy) in [(0, 1), (g.width - 1, -1)]:
            yield ((x, y), (dx, 0))
            yield ((x, y), (0, dy))

    # non-corner edges
    for i in range(g.height):
        for (j, dj) in [(0, 1), (g.width - 1, -1)]:
            yield ((i, j), (0, dj))
    for j in range(g.width):
        for (i, di) in [(0, 1), (g.height - 1, -1)]:
            yield ((i, j), (di, 0))


def solve_part_1(puzzle_input: list[str]):
    g = Grid(puzzle_input)
    return calc_num_energized(g, (0, 0), (0, 1))


def solve_part_2(puzzle_input: list[str]):
    g = Grid(puzzle_input)
    max_energized = 0
    for start_pos, start_dir in all_possible_start_configs(g):
        max_energized = max(max_energized, calc_num_energized(g, start_pos, start_dir))
    return max_energized
