"""
Advent of Code 2024
Day 16: Reindeer Maze
"""

import click
import os
from pathlib import Path
from utils import Grid
from collections import deque, defaultdict


def all_possible_scores(grid: Grid) -> set[int]:
    start = grid.where("S")[0]

    min_scores = {}
    final_scores = set()
    all_locs_in_paths = defaultdict(set)
    q = deque([(start, (0, 1), 0, [start])])

    while q:
        curr, direction, score, path = q.popleft()
        if (curr, direction) in min_scores and score > min_scores[(curr, direction)]:
            continue

        min_scores[(curr, direction)] = score
        i, j = curr
        di, dj = direction
        ni, nj = i + di, j + dj

        if grid.at(ni, nj) == "E":
            final_scores.add(score + 1)
            for loc in path + [(ni, nj)]:
                all_locs_in_paths[score + 1].add(loc)
            continue

        if grid.at(ni, nj) != "#":
            q.append(((ni, nj), direction, score + 1, path + [(ni, nj)]))

        q.append((curr, (-dj, di), score + 1000, path))
        q.append((curr, (dj, -di), score + 1000, path))

    return final_scores, all_locs_in_paths


def solve_part_1(puzzle_input: list[str]):
    grid = Grid(puzzle_input)
    final_scores, _ = all_possible_scores(grid)
    return min(final_scores)


def solve_part_2(puzzle_input: list[str]):
    grid = Grid(puzzle_input)
    final_scores, all_locs_in_paths = all_possible_scores(grid)
    return len(all_locs_in_paths[min(final_scores)])


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
