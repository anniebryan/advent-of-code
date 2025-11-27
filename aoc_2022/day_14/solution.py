"""
Advent of Code 2022
Day 14: Regolith Reservoir
"""

import click
import os
from pathlib import Path


def points(line):
    path = []
    for point in line.split(' -> '):
        x, y = point.split(',')
        path.append((int(x), int(y)))

    start_point = path[0]
    for point in path[1:]:
        x, y = start_point
        if x == point[0]:
            for j in range(min(y, point[1]), max(y, point[1]) + 1):
                yield (x, j)
        if y == point[1]:
            for i in range(min(x, point[0]), max(x, point[0]) + 1):
                yield (i, y)
        start_point = point


def get_rock(input):
    rock = set()
    for line in input:
        for point in points(line):
            rock.add(point)
    xs = {p[0] for p in rock}
    ys = {p[1] for p in rock}
    x_range = (min(xs), max(xs))
    y_range = (min(ys), max(ys))
    return rock, x_range, y_range


def move(sand_loc, rock, sand):
    x, y = sand_loc
    filled = rock.union(sand)

    down = (x, y + 1)
    if down not in filled:
        return down

    diag_left = (x - 1, y + 1)
    if diag_left not in filled:
        return diag_left

    diag_right = (x + 1, y + 1)
    if diag_right not in filled:
        return diag_right
    
    # can't move
    return sand_loc


def print_pile(rock, sand):
    filled = rock.union(sand)
    xs = {p[0] for p in filled}
    ys = {p[1] for p in filled}
    s = []
    for y in range(min(ys), max(ys) + 1):
        for x in range(min(xs), max(xs) + 1):
            if (x, y) in rock:
                s.append("#")
            elif (x, y) in sand:
                s.append("o")
            else:
                s.append(".")
        s.append("\n")
    print("".join(s))
    return


def pour_sand(rock, y_max, sand_start, verbose=False):
    num_sand_dropped = 0
    sand = set()
    done = False
    while not done:
        if num_sand_dropped % 1000 == 0 and verbose:
            print_pile(rock, sand)

        # drop sand
        (prev_sand_loc, sand_loc) = (sand_start, move(sand_start, rock, sand))
        while prev_sand_loc != sand_loc and sand_loc[1] <= y_max:
            (prev_sand_loc, sand_loc) = (sand_loc, move(sand_loc, rock, sand))

        if sand_loc[1] > y_max:
            done = True
        else:
            num_sand_dropped += 1
        if sand_loc == sand_start:
            done = True

        sand.add(sand_loc)
    return num_sand_dropped
        

def solve_part_1(input):
    rock, _, y_range = get_rock(input)
    y_max = y_range[1]
    return pour_sand(rock, y_max, (500, 0))


# TODO speedup
def solve_part_2(input):
    rock, x_range, y_range = get_rock(input)
    x_min, x_max = x_range
    y_min, y_max = y_range

    floor_depth = y_max + 2
    floor = points(f"{500 - floor_depth - 2},{floor_depth} -> {500 + floor_depth + 2},{floor_depth}")
    for point in floor:
        rock.add(point)
    return pour_sand(rock, floor_depth, (500, 0))


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
