"""
Advent of Code 2022
Day 2: Rock Paper Scissors
"""

import os
from pathlib import Path

import click


def get_score(row, part_1):
    opp, me = row.split(" ")
    opp_move = {"A": 0, "B": 1, "C": 2}[opp]

    if part_1:
        move_score = {"X": 1, "Y": 2, "Z": 3}[me]
        outcome_score = 3 * ((move_score - opp_move) % 3)
    else:
        move_score = 1 + (opp_move + {"X": -1, "Y": 0, "Z": 1}[me]) % 3
        outcome_score = {"X": 0, "Y": 3, "Z": 6}[me]
    
    return move_score + outcome_score


def solve_part_1(puzzle_input: list[str]):
    return sum([get_score(row, True) for row in puzzle_input])


def solve_part_2(puzzle_input: list[str]):
    return sum([get_score(row, False) for row in puzzle_input])


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
