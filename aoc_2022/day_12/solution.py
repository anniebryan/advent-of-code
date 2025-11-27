"""
Advent of Code 2022
Day 12: Hill Climbing Algorithm
"""

import click
import os
from pathlib import Path


def create_map(puzzle_input):
    map = {}
    map_size = (0, 0)
    start_loc = None
    end_loc = None
    for i, row in enumerate(puzzle_input):
        for j, val in enumerate(row):
            map_size = (max(map_size[0], i), max(map_size[1], j))
            if val == "S":
                start_loc = (i, j)
                map[(i, j)] = ord('a') - 96
            elif val == "E":
                end_loc = (i, j)
                map[(i, j)] = ord('z') - 96
            else:
                map[(i, j)] = ord(val) - 96
    return (map, map_size, start_loc, end_loc)


def is_valid_neighbor(map, map_size, current_height, neighbor):
    i, j = neighbor
    if 0 <= i <= map_size[0]:
        if 0 <= j <= map_size[1]:
            if current_height + 1 >= map[(i, j)]:
                return True
    return False


def bfs(map, map_size, start_loc, end_loc):
    queue = [start_loc]
    visited = {start_loc}
    dist = {start_loc: 0}

    while queue:
        loc = queue.pop(0)
        x, y = loc
        current_height = map[loc]

        for neighbor in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if is_valid_neighbor(map, map_size, current_height, neighbor):
                if neighbor not in visited:
                    visited.add(neighbor)
                    dist[neighbor] = dist[loc] + 1
                    queue.append(neighbor)

                    if neighbor == end_loc:
                        return dist
    return None


def min_distances(map, map_size, start_locs, end_loc):
    for start_loc in start_locs:
        dist = bfs(map, map_size, start_loc, end_loc)
        if dist is not None:
            yield dist[end_loc]


def solve_part_1(puzzle_input: list[str]):
    map, map_size, start_loc, end_loc = create_map(puzzle_input)
    dist = bfs(map, map_size, start_loc, end_loc)
    if dist is not None:
        return dist[end_loc]
    return "Unable to get to E from S"


def solve_part_2(puzzle_input: list[str]):
    map, map_size, _, end_loc = create_map(puzzle_input)
    d = {}
    for start_loc in map:
        if map[start_loc] == 1:  # valid start location
            dist = bfs(map, map_size, start_loc, end_loc)
            if dist is not None:
                d[start_loc] = dist[end_loc]

    if len(d) == 0:
        return "Unable to get to E from any square at elevation a"
    best_start_loc = min(d, key=d.get)
    return f"Starting from {best_start_loc} gives a min distance of {d[best_start_loc]}"


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
