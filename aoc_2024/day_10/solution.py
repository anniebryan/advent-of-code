"""
Advent of Code 2024
Day 10: Hoof It
"""

import click
import os
import pathlib
from utils import DirectedGraph


def parse_input(puzzle_input: list[str]):
    loc_to_val = {}
    for i, row in enumerate(puzzle_input):
        for j, val in enumerate(row):
            loc_to_val[(i, j)] = val

    g = DirectedGraph()
    for i, row in enumerate(puzzle_input):
        for j, val in enumerate(row):
            if val != ".":
                for (di, dj) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                    neighbor = (i + di, j + dj)
                    if neighbor in loc_to_val and loc_to_val[neighbor] != "." and int(loc_to_val[neighbor]) == int(val) + 1:
                        g.insert_edge((i, j), neighbor)                    
    return g, loc_to_val


def path_exists(g: DirectedGraph, start: tuple[int, int], end: tuple[int, int], memo) -> bool:
    if (start, end) in memo:
        return memo[(start, end)]

    if start == end:
        memo[(start, end)] = True
        return True

    for n in g.graph[start]:
        if path_exists(g, n, end, memo):
            memo[(start, end)] = True
            return True

    memo[(start, end)] = False
    return False


def num_paths(g: DirectedGraph, start: tuple[int, int], end: tuple[int, int], memo) -> int:
    if (start, end) in memo:
        return memo[(start, end)]

    if start == end:
        memo[(start, end)] = 1
        return 1

    ans = sum([num_paths(g, n, end, memo) for n in g.graph[start]])
    memo[(start, end)] = ans
    return ans


def get_start_end_locs(loc_to_val):
    start_locs = {loc for loc, val in loc_to_val.items() if val == "0"}
    end_locs = {loc for loc, val in loc_to_val.items() if val == "9"}
    return start_locs, end_locs


def solve_part_1(puzzle_input: list[str]):
    g, loc_to_val = parse_input(puzzle_input)
    start_locs, end_locs = get_start_end_locs(loc_to_val)
    total_score = 0
    for start in start_locs:
        for end in end_locs:
            if path_exists(g, start, end, {}):
                total_score += 1
    return total_score


def solve_part_2(puzzle_input: list[str]):
    g, loc_to_val = parse_input(puzzle_input)
    start_locs, end_locs = get_start_end_locs(loc_to_val)
    total_rating = 0
    for start in start_locs:
        for end in end_locs:
            total_rating += num_paths(g, start, end, {})
    return total_rating


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
