"""
Advent of Code 2023
Day 16: The Floor Will Be Lava
"""

from typing import Iterator
import click
import os
from pathlib import Path
from utils import Grid
from collections import deque


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
