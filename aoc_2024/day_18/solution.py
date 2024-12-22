"""
Advent of Code 2024
Day 18: RAM Run
"""

import click
import os
import pathlib
from utils import Grid


def parse_input(puzzle_input: list[str]):
    n_bytes = int(puzzle_input[0])
    coords = set()
    for line in puzzle_input[1:n_bytes + 1]:
        a, b = line.split(",")
        coords.add((int(a), int(b)))
    remaining = []
    for line in puzzle_input[n_bytes + 1:]:
        a, b = line.split(",")
        remaining.append((int(a), int(b)))
    return coords, remaining


def coords_to_grid(coords: set[tuple[int, int]]) -> Grid:
    width = max(coords, key=lambda c: c[0])[0]
    height = max(coords, key=lambda c: c[1])[1]
    grid_input = []
    for y in range(height + 1):
        row = []
        for x in range(width + 1):
            if (x, y) in coords:
                row.append("#")
            else:
                row.append(".")
        grid_input.append("".join(row))
    return Grid(grid_input)


def path_exists(grid: Grid, start: tuple[int, int], end: tuple[int, int]) -> bool:
    dists = grid.dijkstra(start)
    return end in dists


def solve_part_1(puzzle_input: list[str]):
    coords, _ = parse_input(puzzle_input)
    grid = coords_to_grid(coords)
    start = (0, 0)
    end = (grid.width - 1, grid.height - 1)
    return grid.dijkstra(start)[end]


def solve_part_2(puzzle_input: list[str]):
    coords, remaining = parse_input(puzzle_input)
    grid = coords_to_grid(coords)
    start = (0, 0)
    end = (grid.width - 1, grid.height - 1)
    for (ri, rj) in remaining:
        grid.set(rj, ri, "#")
        if not path_exists(grid, start, end):
            return (ri, rj)


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
