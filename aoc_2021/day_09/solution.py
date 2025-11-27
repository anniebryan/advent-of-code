"""
Advent of Code 2021
Day 9: Smoke Basin
"""

import click
import os
from pathlib import Path
from math import prod


def get_heightmap_dict(puzzle_input):
    heightmap = [[int(val) for val in row.strip()] for row in puzzle_input]
    num_rows = len(heightmap)
    num_cols = len(heightmap[0])
    heightmap_dict = {(i, j): heightmap[j][i] for i in range(num_cols) for j in range(num_rows)}
    return heightmap_dict, num_rows, num_cols


def horizontal_neighbor_locs(num_cols, i, j):
    left, right = (i - 1, j), (i + 1, j)
    locs = set()
    if i != 0:
        locs.add(left)
    if i != num_cols - 1:
        locs.add(right)
    return locs


def vertical_neighbor_locs(num_rows, i, j):
    up, down = (i, j - 1), (i, j + 1)
    locs = set()
    if j != 0:
        locs.add(up)
    if j != num_rows - 1:
        locs.add(down)
    return locs


def is_low_point(heightmap_dict, num_rows, num_cols, i, j):
    val = heightmap_dict[(i, j)]
    neighbors = horizontal_neighbor_locs(num_cols, i, j) | vertical_neighbor_locs(num_rows, i, j)
    return all([val < heightmap_dict[n] for n in neighbors])


def expand_basin_horizontally(heightmap_dict, num_cols, i, j):
    basin = {(i, j)}
    val = heightmap_dict[(i, j)]
    neighbors = horizontal_neighbor_locs(num_cols, i, j)
    add_to_basin = {v for v in neighbors if val < heightmap_dict[v] and heightmap_dict[v] != 9}
    for loc in add_to_basin:
        basin |= expand_basin_horizontally(heightmap_dict, num_cols, *loc)
    return basin


def expand_basin_vertically(heightmap_dict, num_rows, i, j):
    basin = {(i, j)}
    val = heightmap_dict[(i, j)]
    neighbors = vertical_neighbor_locs(num_rows, i, j)
    basin |= {v for v in neighbors if val < heightmap_dict[v] and heightmap_dict[v] != 9}
    return basin


def create_basin(heightmap_dict, num_rows, num_cols, i, j):
    basin = expand_basin_horizontally(heightmap_dict, num_cols, i, j)
    prev_size = len(basin)
    finished = False

    while not finished:
        expand_vertically = set()
        for loc in basin:
            expand_vertically |= expand_basin_vertically(heightmap_dict, num_rows, *loc)
        basin |= expand_vertically

        expand_horizontally = set()
        for loc in basin:
            expand_horizontally |= expand_basin_horizontally(heightmap_dict, num_cols, *loc)
        basin |= expand_horizontally

        new_size = len(basin)
        finished = (new_size == prev_size)
        prev_size = new_size

    return basin


def get_low_points(heightmap_dict, num_rows, num_cols):
    return [loc for loc in heightmap_dict.keys() if is_low_point(heightmap_dict, num_rows, num_cols, *loc)]


def solve_part_1(puzzle_input: list[str]):
    heightmap_dict, num_rows, num_cols = get_heightmap_dict(puzzle_input)
    low_points = get_low_points(heightmap_dict, num_rows, num_cols)
    return sum([1 + heightmap_dict[loc] for loc in low_points])


def solve_part_2(puzzle_input: list[str]):
    heightmap_dict, num_rows, num_cols = get_heightmap_dict(puzzle_input)
    low_points = get_low_points(heightmap_dict, num_rows, num_cols)
    basin_sizes = [len(create_basin(heightmap_dict, num_rows, num_cols, *loc)) for loc in low_points]
    three_largest_basins = sorted(basin_sizes, reverse=True)[:3]
    return prod(three_largest_basins)


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
