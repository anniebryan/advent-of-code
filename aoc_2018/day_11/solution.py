"""
Advent of Code 2018
Day 11: Chronal Charge
"""

import click
import os
from pathlib import Path
import numpy as np


def get_serial_number(puzzle_input):
    serial_number = int(puzzle_input[0])
    return serial_number


def get_power_level(x, y, serial_number):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    hundreds_digit = (power_level // 100) % 10
    return hundreds_digit - 5


def get_total_power(top_left_x, top_left_y, size, serial_number):
    total_power = 0
    for i in range(size):
        for j in range(size):
            x = top_left_x + i
            y = top_left_y + j
            total_power += get_power_level(x, y, serial_number)
    return total_power


def find_largest_total_power(size, serial_number):
    max_power = get_total_power(0, 0, size, serial_number)
    best_i, best_j = 0, 0
    for i in range(300 - size):
        for j in range(300 - size):
            total_power = get_total_power(i, j, size, serial_number)
            if total_power > max_power:
                max_power = total_power
                best_i, best_j = i, j
    return best_i, best_j


def consider_all_sizes(serial_number):
    powers = np.fromfunction(lambda i, j: get_power_level(i, j, serial_number), (300, 300))
    best_size, max_power, best_x, best_y = 0, 0, 0, 0
    for size in range(1, 300):
        boxes = sum([powers[x:x - size, y:y - size] for x in range(size) for y in range(size)])
        power = int(boxes.max())
        if power > max_power:
            max_power = power
            best_size = size
            best_x, best_y = np.where(boxes == max_power)
    return int(best_x[0]), int(best_y[0]), best_size


def solve_part_1(puzzle_input: list[str]):
    serial_number = get_serial_number(puzzle_input)
    return find_largest_total_power(3, serial_number)


def solve_part_2(puzzle_input: list[str]):
    serial_number = get_serial_number(puzzle_input)
    return consider_all_sizes(serial_number)


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
