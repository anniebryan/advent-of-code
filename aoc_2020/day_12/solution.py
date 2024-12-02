"""
Advent of Code 2020
Day 12: Rain Risk
"""

import click
import os
import pathlib


def get_instructions(puzzle_input):
    return [(line[0], int(line[1:])) for line in puzzle_input]


def process_instruction(instruction, direction, x, y):
    action, val = instruction[0], instruction[1]
    if action == 'N' or (action == 'F' and direction == 90):
        return direction, x, y + val
    elif action == 'S' or (action == 'F' and direction == 270):
        return direction, x, y - val
    elif action == 'E' or (action == 'F' and direction == 0):
        return direction, x + val, y
    elif action == 'W' or (action == 'F' and direction == 180):
        return direction, x - val, y
    elif action == 'L':
        return (direction + val) % 360, x, y
    elif action == 'R':
        return (direction - val) % 360, x, y


def process_waypoint(instruction, x, y, way_x, way_y):
    action, val = instruction[0], instruction[1]
    if action == 'N':
        return x, y, way_x, way_y + val
    elif action == 'S':
        return x, y, way_x, way_y - val
    elif action == 'E':
        return x, y, way_x + val, way_y
    elif action == 'W':
        return x, y, way_x - val, way_y
    elif (action == 'L' and val == 90)  or (action == 'R' and val == 270):
        return x, y, -way_y, way_x
    elif (action == 'L' and val == 270) or (action == 'R' and val == 90):
        return x, y, way_y, -way_x
    elif (action == 'L' or action == 'R') and val == 180:
        return x, y, -way_x, -way_y
    elif action == 'F':
        return x + way_x * val, y + way_y * val, way_x, way_y


def process_all_instructions(puzzle_input, part_one):
    instructions = get_instructions(puzzle_input)
    x, y = 0, 0
    if part_one:
        direction = 0
        for instruction in instructions:
            direction, x, y = process_instruction(instruction, direction, x, y)
    else:
        way_x, way_y = 10, 1
        for instruction in instructions:
            x, y, way_x, way_y = process_waypoint(instruction, x, y, way_x, way_y)
    return x, y


def manhattan_distance(x, y):
    return abs(x) + abs(y)


def solve_part_1(puzzle_input: list[str]):
    final_x, final_y = process_all_instructions(puzzle_input, True)
    return manhattan_distance(final_x, final_y)


def solve_part_2(puzzle_input: list[str]):
    final_x, final_y = process_all_instructions(puzzle_input, False)
    return manhattan_distance(final_x, final_y)


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
