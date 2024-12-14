"""
Advent of Code 2023
Day 14: Parabolic Reflector Dish
"""

import copy
from enum import Enum
import click
import os
import pathlib
from utils import Grid
from typing import Literal


def tilt(g: Grid, direction: Literal["N", "S", "E", "W"]) -> Grid:
    if direction == "N":
        for j in range(g.width):
            cube_ixs = [i for i in range(g.height) if g.at(i, j) == "#"][::-1]
            for a, b in zip([g.height] + cube_ixs, cube_ixs + [-1]):
                num_round_rocks = len([i for i in range(a - 1, b, -1) if g.at(i, j) == "O"])
                for i in range(a - 1, b + num_round_rocks, -1):
                    g.set(i, j, ".")
                for i in range(b + num_round_rocks, b, -1):
                    g.set(i, j, "O")

    elif direction == "S":
        for j in range(g.width):
            cube_ixs = [i for i in range(g.height) if g.at(i, j) == "#"]
            for a, b in zip([-1] + cube_ixs, cube_ixs + [g.height]):
                num_round_rocks = len([i for i in range(a + 1, b) if g.at(i, j) == "O"])
                for i in range(a + 1, b - num_round_rocks):
                    g.set(i, j, ".")
                for i in range(b - num_round_rocks, b):
                    g.set(i, j, "O")

    elif direction == "E":
        for i in range(g.height):
            cube_ixs = [j for j in range(g.width) if g.at(i, j) == "#"]
            for a, b in zip([-1] + cube_ixs, cube_ixs + [g.width]):
                num_round_rocks = len([j for j in range(a + 1, b) if g.at(i, j) == "O"])
                for j in range(a + 1, b - num_round_rocks):
                    g.set(i, j, ".")
                for j in range(b - num_round_rocks, b):
                    g.set(i, j, "O")

    elif direction == "W":
        for i in range(g.height):
            cube_ixs = [j for j in range(g.width) if g.at(i, j) == "#"][::-1]
            for a, b in zip([g.width] + cube_ixs, cube_ixs + [-1]):
                num_round_rocks = len([j for j in range(a - 1, b, -1) if g.at(i, j) == "O"])
                for j in range(a - 1, b + num_round_rocks, -1):
                    g.set(i, j, ".")
                for j in range(b + num_round_rocks, b, -1):
                    g.set(i, j, "O")
    return g


def total_load(g: Grid) -> int:
    tot = 0
    for j in range(g.width):
        for i in range(g.height):
            if g.at(i, j) == "O":
                tot += (g.height - i)
    return tot


def cycle_n_times(g: Grid, n: int) -> Grid:
    g_to_ix = {str(g): 0}
    ix_to_g = {0: g}

    for i in range(1, n + 1):
        for direction in "NWSE":
            g = tilt(g, direction)

        # detect cycle
        if str(g) in g_to_ix:
            prev_i = g_to_ix[str(g)]
            return ix_to_g[((n - i) % (i - prev_i)) + prev_i]

        g_to_ix[str(g)] = i
        ix_to_g[i] = copy.deepcopy(g)

    return g


def solve_part_1(puzzle_input: list[str]):
    g = Grid(puzzle_input)
    g = tilt(g, "N")
    return total_load(g)


def solve_part_2(puzzle_input: list[str]):
    g = Grid(puzzle_input)
    g = cycle_n_times(g, 1000000000)
    return total_load(g)


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


"""
.....#....
....#...O#
.....##...
...#......
.....OOO#.
.O#...O#.#
....O#...O
......OOOO
#....###.O
#.OOO#..OO

.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O

"""