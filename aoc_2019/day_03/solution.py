"""
Advent of Code 2019
Day 3: Crossed Wires
"""

import os
from pathlib import Path

import click


def get_wires(puzzle_input):
    wire_1, wire_2 = [[(i[0], int(i[1:])) for i in row.split(",")] for row in puzzle_input]
    return wire_1, wire_2


def combine(loc, dir):
    change_by = {'L': (-1, 0), 'R':(1, 0), 'U':(0, 1), 'D':(0, -1)}
    new_loc = tuple(loc[i] + change_by[dir[0]][i] * dir[1] for i in range(2))
    return new_loc


def get_vertices(wire, current_loc = (0,0)):
    if not wire:
        return [current_loc]
    new_loc = combine(current_loc, wire[0])
    return [current_loc] + get_vertices(wire[1:], new_loc)


def get_path(vertices):
    if len(vertices) < 2:
        return []
    if vertices[0][0] == vertices[1][0]:
        if vertices[0][1] < vertices[1][1]:
            path = [(vertices[0][0], i + 1) for i in range(vertices[0][1], vertices[1][1])]
        else:
            path = [(vertices[0][0], i) for i in range(vertices[1][1], vertices[0][1])][::-1]
    else:
        if vertices[0][0] < vertices[1][0]:
            path = [(i + 1, vertices[0][1]) for i in range(vertices[0][0], vertices[1][0])]
        else:
            path = [(i, vertices[0][1]) for i in range(vertices[1][0], vertices[0][0])][::-1]
    return path + get_path(vertices[1:])


def get_manhattan_distance(loc):
    return abs(loc[0]) + abs(loc[1])


def get_intersections(wire_1, wire_2):
    path_1 = set(get_path(get_vertices(wire_1)))
    path_2 = set(get_path(get_vertices(wire_2)))
    intersections = path_1 & path_2
    return intersections


def solve_part_1(puzzle_input: list[str]):
    wire_1, wire_2 = get_wires(puzzle_input)
    distances = {get_manhattan_distance(i):i for i in get_intersections(wire_1, wire_2)}
    return min(distances)


def get_steps_so_far(path1, path2, loc):
    return path1.index(loc) + path2.index(loc) + 2


def solve_part_2(puzzle_input: list[str]):
    wire_1, wire_2 = get_wires(puzzle_input)
    v1 = get_path(get_vertices(wire_1))
    v2 = get_path(get_vertices(wire_2))
    steps_so_far = {get_steps_so_far(v1,v2,i):i for i in get_intersections(wire_1, wire_2)}
    return min(steps_so_far)


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
