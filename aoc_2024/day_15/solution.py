"""
Advent of Code 2024
Day 15: Warehouse Woes
"""

import click
import os
from pathlib import Path
from utils import Grid

MOVE_TO_DIR = {
    ">": (0, 1),
    "<": (0, -1),
    "v": (1, 0),
    "^": (-1, 0),
}


def parse_input(puzzle_input: list[str], part_2: bool):
    empty_line_ix = [ix for ix, row in enumerate(puzzle_input) if row == ""][0]
    grid_rows = puzzle_input[:empty_line_ix]
    if part_2:
        grid_rows = [row.replace("#", "##").replace(".", "..").replace("O", "[]").replace("@", "@.") for row in grid_rows]
    grid = Grid(grid_rows)
    moves = "".join(puzzle_input[empty_line_ix + 1:])
    return grid, moves


def move_robot(grid: Grid, robot: tuple[int, int], move: str, part_2: bool) -> tuple[int, int]:
    move_i, move_j = MOVE_TO_DIR[move]
    robot_i, robot_j = robot
    new_i, new_j = robot_i + move_i, robot_j + move_j
    if grid.at(new_i, new_j) == ".":
        grid.set(robot_i, robot_j, ".")
        grid.set(new_i, new_j, "@")
        return (new_i, new_j)
    elif grid.at(new_i, new_j) == "#":
        return (robot_i, robot_j)
    else:
        if part_2:
            assert grid.at(new_i, new_j) in "[]"
            if grid.at(new_i, new_j) == "[":
                square_locs_to_shift = {(new_i, new_j), (new_i, new_j + 1)}
            else:
                square_locs_to_shift = {(new_i, new_j - 1), (new_i, new_j)}

            new_locs = {(s_i + move_i, s_j + move_j) for (s_i, s_j) in square_locs_to_shift} - square_locs_to_shift
            while True:
                if any(grid.at(n_i, n_j) == "#" for (n_i, n_j) in new_locs):
                    return (robot_i, robot_j)
                if all(grid.at(n_i, n_j) == "." for (n_i, n_j) in new_locs):
                    current_grid_values = {(i, j): grid.at(i, j) for (i, j) in square_locs_to_shift}
                    for (c_i, c_j) in square_locs_to_shift:
                        grid.set(c_i, c_j, ".")
                    for (c_i, c_j) in square_locs_to_shift:
                        grid.set(c_i + move_i, c_j + move_j, current_grid_values[(c_i, c_j)])
                    grid.set(new_i, new_j, "@")
                    grid.set(robot_i, robot_j, ".")
                    return (new_i, new_j)
                for (n_i, n_j) in new_locs:
                    if grid.at(n_i, n_j) == "[":
                        square_locs_to_shift.add((n_i, n_j))
                        square_locs_to_shift.add((n_i, n_j + 1))
                    elif grid.at(n_i, n_j) == "]":
                        square_locs_to_shift.add((n_i, n_j))
                        square_locs_to_shift.add((n_i, n_j - 1))
                new_locs = {(s_i + move_i, s_j + move_j) for (s_i, s_j) in square_locs_to_shift} - square_locs_to_shift
        else:
            assert grid.at(new_i, new_j) == "O"
            next_i, next_j = new_i, new_j
            while grid.at(next_i, next_j) == "O":
                next_i += move_i
                next_j += move_j
            if grid.at(next_i, next_j) == "#":
                return (robot_i, robot_j)
            else:
                assert grid.at(next_i, next_j) == "."
                grid.set(next_i, next_j, "O")
                grid.set(new_i, new_j, "@")
                grid.set(robot_i, robot_j, ".")
                return (new_i, new_j)
        

def tot_gps_coords(grid: Grid, part_2: bool) -> int:
    tot = 0
    for i in range(grid.height):
        for j in range(grid.width):
            if part_2:
                if grid.at(i, j) == "[":
                    tot += 100 * i + j
            else:
                if grid.at(i, j) == "O":
                    tot += 100 * i + j
    return tot


def solve_part_1(puzzle_input: list[str]):
    grid, moves = parse_input(puzzle_input, False)
    robot = grid.where("@")[0]

    for move in moves:
        robot = move_robot(grid, robot, move, False)

    return tot_gps_coords(grid, False)


def solve_part_2(puzzle_input: list[str]):
    grid, moves = parse_input(puzzle_input, True)
    robot = grid.where("@")[0]

    for move in moves:
        robot = move_robot(grid, robot, move, True)

    return tot_gps_coords(grid, True)


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
