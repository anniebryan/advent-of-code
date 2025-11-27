"""
Advent of Code 2020
Day 15: Rambunctious Recitation
"""

import os
from pathlib import Path

import click


def process_input(puzzle_input):
    numbers = puzzle_input[0].split(",")
    history = {int(n): i + 1 for i, n in enumerate(numbers)}
    last_turn = int(numbers[-1])
    i = len(numbers) + 1
    return history, last_turn, i


def take_turn(history, last_turn, i):
    """
    history: dictionary mapping a number to the index of the most recent turn that number was spoken
            (if a number has never been spoken, it will not be a key of the dictionary)
    last_turn: the number most recently spoken
    i: the number corresponding to the current turn
    """
    spoken = i - 1 - history[last_turn] if last_turn in history else 0
    history[last_turn] = i - 1
    return history, spoken, i + 1


def nth_number_spoken(puzzle_input, n):
    history, last_turn, i = process_input(puzzle_input)
    while i <= n:
        history, last_turn, i = take_turn(history, last_turn, i)
    return last_turn


def solve_part_1(puzzle_input: list[str]):
    return nth_number_spoken(puzzle_input, 2020)


def solve_part_2(puzzle_input: list[str]):
    return nth_number_spoken(puzzle_input, 30000000)


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
