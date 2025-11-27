"""
Advent of Code 2024
Day 4
"""

import os
from pathlib import Path

import click


def parse_input(puzzle_input: list[str]):
    graph = {}
    for i, row in enumerate(puzzle_input):
        for j, ch in enumerate(row):
            graph[(i, j)] = ch
    return graph


def solve_part_1(puzzle_input: list[str]):
    graph = parse_input(puzzle_input, False)
    valid_words = {"XMAS", "SAMX"}
    num_xmas = 0
    for i in range(len(puzzle_input)):
        for j in range(len(puzzle_input[i]) - 3):
            word = "".join([graph[(i, j + x)] for x in range(4)])
            num_xmas += (word in valid_words)
    for i in range(len(puzzle_input) - 3):
        for j in range(len(puzzle_input[i])):
            word = "".join([graph[(i + x, j)] for x in range(4)])
            num_xmas += (word in valid_words)
    for i in range(len(puzzle_input) - 3):
        for j in range(len(puzzle_input[i]) - 3):
            word = "".join([graph[(i + x, j + x)] for x in range(4)])
            num_xmas += (word in valid_words)
    for i in range(3, len(puzzle_input)):
        for j in range(len(puzzle_input[i]) - 3):
            word = "".join([graph[(i - x, j + x)] for x in range(4)])
            num_xmas += (word in valid_words)
    return num_xmas


def solve_part_2(puzzle_input: list[str]):
    graph = parse_input(puzzle_input, True)
    valid_words = {"MAS", "SAM"}
    num_xmas = 0
    for i in range(len(puzzle_input) - 2):
        for j in range(len(puzzle_input) - 2):
            word_1 = "".join([graph[(i + x, j + x)] for x in range(3)])
            word_2 = "".join([graph[(i + 2 - x, j + x)] for x in range(3)])
            num_xmas += (word_1 in valid_words and word_2 in valid_words)
    return num_xmas


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
