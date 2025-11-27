"""
Advent of Code 2021
Day 13: Transparent Origami
"""

import click
import os
from pathlib import Path


def get_dots_instructions(puzzle_input):
    dots, instructions = [], []
    is_instruction = False
    for line in puzzle_input:
        if line == "":
            is_instruction = True
        elif is_instruction:
            instructions.append(tuple([line.split('=')[0][-1], int(line.split('=')[1])]))
        else:
            dots.append(tuple([int(val) for val in line.split(',')]))
    return dots, instructions


def fold(dots, dir, val):
    new_dots = set()
    for dot in dots:
        x, y = dot
        if dir == 'x':
            new_x = x if val > x else 2 * val - x
            new_dot = (new_x, y)
        else:
            new_y = y if val > y else 2 * val - y
            new_dot = (x, new_y)
        new_dots.add(new_dot)
    return new_dots


def visualize(dots):
    max_x = max([dot[0] for dot in dots])
    max_y = max([dot[1] for dot in dots])

    s = ["\n"]
    for j in range(max_y + 1):
        row = ["#" if (i, j) in dots else "." for i in range(max_x + 1)]
        s.append("".join(row))
    return "\n".join(s)


def solve_part_1(puzzle_input: list[str]):
    dots, instructions = get_dots_instructions(puzzle_input)
    dir, val = instructions[0]
    return len(fold(dots, dir, val))


def solve_part_2(puzzle_input: list[str]):
    dots, instructions = get_dots_instructions(puzzle_input)
    for instruction in instructions:
        dir, val = instruction
        dots = fold(dots, dir, val)
    return visualize(dots)


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
