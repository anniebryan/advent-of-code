"""
Advent of Code 2020
Day 23: Crab Cups
"""

import click
import os
import pathlib


def get_initial_cups(puzzle_input, num_cups):
    if num_cups is None: num_cups = len(puzzle_input[0])
    vals = [int(n) for n in puzzle_input[0]]
    cups = {}
    for i in range(len(vals)-1):
        cups[vals[i]] = vals[i + 1]

    cups[vals[-1]] = len(vals) + 1 if num_cups > len(vals) else vals[0]

    for i in range(len(vals) + 1, num_cups):
        cups[i] = i + 1

    if num_cups > len(vals):
        cups[num_cups] = vals[0]
        
    return cups, vals[0]


def make_move(cups, current_cup):
    a = cups[current_cup]
    b = cups[a]
    c = cups[b]
    removed = {a, b, c}

    destination_cup = current_cup - 1 if current_cup > 1 else max(cups)
    while destination_cup in removed:
        destination_cup = destination_cup - 1 if destination_cup > 1 else max(cups)

    cups[current_cup] = cups[c]
    cups[c] = cups[destination_cup]
    cups[destination_cup] = a

    current_cup = cups[current_cup]
    return cups, current_cup


def make_n_moves(puzzle_input, num_rounds, num_cups=None):
    cups, current_cup = get_initial_cups(puzzle_input, num_cups)
    for _ in range(num_rounds):
        cups, current_cup = make_move(cups, current_cup)
    return cups


def list_starting_at(cups, start):
    s = ""
    cup = cups[start]
    while cup != start:
        s += str(cup)
        cup = cups[cup]
    return s


def get_clockwise(cups, start):
    a = cups[start]
    b = cups[a]
    return (a, b)


def solve_part_1(puzzle_input: list[str]):
    cups = make_n_moves(puzzle_input, 100)
    return list_starting_at(cups, 1)


def solve_part_2(puzzle_input: list[str]):
    cups = make_n_moves(puzzle_input, 10000000, 1000000)
    a, b = get_clockwise(cups, 1)
    return f"{a} * {b} = {a * b}"


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
