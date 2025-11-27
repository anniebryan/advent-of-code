"""
Advent of Code 2023
Day 13: Point of Incidence
"""

import click
import os
from pathlib import Path
from collections import defaultdict
from typing import Iterable


def parse_input(puzzle_input: list[str]):
    i = 1
    rows = {}
    cols = defaultdict(list)
    for row in puzzle_input:
        if row == "":
            cols = {i: "".join(col) for i, col in cols.items()}
            yield rows, cols
            i = 1
            rows = {}
            cols = defaultdict(list)
            continue
        rows[i] = row
        for j, val in enumerate(row):
            cols[j + 1].append(val)
        i += 1
    cols = {i: "".join(col) for i, col in cols.items()}
    yield rows, cols


def lines_different(d: dict[int, str], indices_equal: dict[tuple[int, int]: bool], mirror: int) -> int:
    lines = set()
    i = mirror
    j = mirror + 1
    while i >= 1 and j <= len(d):
        if not indices_equal[(i, j)]:
            lines.add((i, j))
        i -= 1
        j += 1
    return lines


def num_chars_different(a: str, b: str) -> int:
    num = 0
    for sa, sb in zip(a, b):
        if sa != sb:
            num += 1
    return num


def get_mirror(d: dict[int, str]) -> int:
    indices_equal = {(i, j): d[i] == d[j] for i in d for j in d}
    for mirror in range(1, len(d)):
        if len(lines_different(d, indices_equal, mirror)) == 0:
            return mirror
    return None


def get_new_mirror(d: dict[int, str]) -> int:
    indices_equal = {(i, j): d[i] == d[j] for i in d for j in d}
    for mirror in range(1, len(d)):
        l = lines_different(d, indices_equal, mirror)
        if len(l) == 1:
            a, b = min(l)
            if num_chars_different(d[a], d[b]) == 1:
                return mirror
    return None


def calc_total(mirrors: Iterable) -> int:
    tot = 0
    for horiz_mirror, vert_mirror in mirrors:
        if horiz_mirror is not None:
            tot += horiz_mirror * 100
        if vert_mirror is not None:
            tot += vert_mirror
    return tot


def solve_part_1(puzzle_input: list[str]) -> int:
    mirrors = ((get_mirror(rows), get_mirror(cols)) for rows, cols in parse_input(puzzle_input))
    return calc_total(mirrors)


def solve_part_2(puzzle_input: list[str]) -> int:
    mirrors = ((get_new_mirror(rows), get_new_mirror(cols)) for rows, cols in parse_input(puzzle_input))
    return calc_total(mirrors)


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
