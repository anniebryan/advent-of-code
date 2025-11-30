"""
Advent of Code 2024
Day 18: RAM Run
"""

from aoc_utils import Grid


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
