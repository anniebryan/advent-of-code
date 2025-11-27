"""
Advent of Code 2024
Day 20: Race Condition
"""

import os
from collections import defaultdict, deque
from pathlib import Path
from typing import Iterable

import click

from utils import Grid


def neighbors(g: Grid, loc: tuple[int, int]) -> Iterable[tuple[int, int]]:
    i, j = loc
    for ni, nj in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        if g.in_bounds(ni, nj):
            yield (ni, nj)


def bfs(g: Grid, start: tuple[int, int], max_cheat_len: int) -> Iterable[tuple[int, int]]:
    """Yields locs (i, j) where `g.at(i, j)` is either "." or "E" which can be reached from `start`
    in at most `max_cheat_len` steps through a path consisting of only '#' spaces."""
    q = deque([(start, max_cheat_len)])
    seen = set()
    while q:
        (curr, l) = q.popleft()
        for (ni, nj) in neighbors(g, curr):
            if (ni, nj) not in seen:
                seen.add((ni, nj))
                if g.at(ni, nj) in ".E":
                    yield (ni, nj)
                if l > 1 and g.at(ni, nj) == "#":
                    q.append(((ni, nj), max_cheat_len - 1))


def get_times_saved(g: Grid, max_cheat_len: int) -> dict[int, int]:
    start = g.where("S")[0]
    end = g.where("E")[0]

    dists_from_start = g.dijkstra(start)
    dists_from_end = g.dijkstra(end)
    len_without_cheating = dists_from_start[end]

    path = sorted(dists_from_start, key=dists_from_start.get)

    time_saved_dict = defaultdict(int)
    for start_t, start in enumerate(path):
        for end_t, end in enumerate(path):
            if start_t + 3 <= end_t:
                cheat_len = abs(end[0] - start[0]) + abs(end[1] - start[1])
                dist_with_cheat = start_t + cheat_len + dists_from_end[end]
                if cheat_len <= max_cheat_len and start_t + cheat_len < end_t:
                    time_saved = len_without_cheating - dist_with_cheat
                    time_saved_dict[time_saved] += 1
    return time_saved_dict


def display_res(time_saved_dict: dict[int, int]) -> None:
    for t in sorted(time_saved_dict):
        num_cheats = time_saved_dict[t]
        if t > 0:
            if num_cheats > 1:
                print(f"There are {num_cheats} cheats that save {t} picoseconds.")
            elif num_cheats == 1:
                print(f"There is one cheat that saves {t} picoseconds.")


def num_cheats(puzzle_input: list[str], max_cheat_len: int, picoseconds_saved: int) -> int:
    verbose = (puzzle_input[0] == "T")
    g = Grid(puzzle_input[1:])
    time_saved_dict = get_times_saved(g, max_cheat_len)

    if verbose:
        display_res(time_saved_dict)

    return sum([v for k, v in time_saved_dict.items() if k >= picoseconds_saved])


def solve_part_1(puzzle_input: list[str]):
    return num_cheats(puzzle_input, 2, 100)


def solve_part_2(puzzle_input: list[str]):
    return num_cheats(puzzle_input, 20, 100)


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
