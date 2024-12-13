"""
Advent of Code 2024
Day 12
"""

import click
import os
import pathlib
from collections import deque, defaultdict
from collections.abc import Iterator


class Grid:
    def __init__(self, puzzle_input: list[str]):
        self.values = {}
        for i, row in enumerate(puzzle_input):
            for j, val in enumerate(row):
                self.values[(i, j)] = val
    
    def at(self, i: int, j: int) -> str:
        return self.values[(i, j)]
    
    def in_bounds(self, i: int, j: int) -> bool:
        return (i, j) in self.values
    
    def __iter__(self):
        for (i, j) in sorted(self.values.keys()):
            yield (i, j)


def fill_region(g: Grid, i: int, j: int) -> set[tuple[int, int]]:
    # BFS
    region = {(i, j)}
    q = deque([(i, j)])
    while q:
        (ci, cj) = q.popleft()
        for (di, dj) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            x, y = ci + di, cj + dj
            if (x, y) not in region and g.in_bounds(x, y) and g.at(x, y) == g.at(ci, cj):
                region.add((x, y))
                q.append((x, y))
    return region


def get_all_regions(puzzle_input: list[str]) -> Iterator[tuple[int, int]]:
    g = Grid(puzzle_input)
    all_seen = set()
    for (i, j) in g:
        if (i, j) in all_seen:
            continue
        region = fill_region(g, i, j)
        yield region
        all_seen |= region


def calc_perimeter(region: set[tuple[int, int]]) -> int:
    perim = 0
    locs_counted = set()
    for (i, j) in region:
        num_neighbors_counted = 0
        for (di, dj) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            if (i + di, j + dj) in locs_counted:
                num_neighbors_counted += 1
        perim += 4 - (2 * num_neighbors_counted)
        locs_counted.add((i, j))
    return perim


def get_dir(curr, prev) -> str:
    """Return "UD" for up and down, "LR" for left and right"""
    if prev is None:
        return None
    (ci, cj) = curr
    (pi, pj) = prev
    if ci == pi:
        return "LR"
    if cj == pj:
        return "UD"
    raise ValueError(f"Unexpected {curr=} {prev=}")


def calc_num_sides(region: set[tuple[int, int]]) -> int:
    # TODO
    raise NotImplementedError


def solve_part_1(puzzle_input: list[str]):
    tot = 0
    for region in get_all_regions(puzzle_input):
        area = len(region)
        perimeter = calc_perimeter(region)
        tot += area * perimeter
    return tot


def solve_part_2(puzzle_input: list[str]):
    tot = 0
    # for region in get_all_regions(puzzle_input):
    #     area = len(region)
    #     num_sides = calc_num_sides(region)
    #     tot += area * num_sides
    return tot


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
