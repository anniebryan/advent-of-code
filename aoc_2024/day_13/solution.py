"""
Advent of Code 2024
Day 13: Claw Contraption
"""

import click
import os
from pathlib import Path
import regex as re

COST = {"A": 3, "B": 1}
MAX_PRESSES = 100
PRIZE_OFFSET = 10000000000000


def parse_input(puzzle_input: list[str]):
    for i in range(0, len(puzzle_input), 4):
        a_match = re.match(r"X\+(?P<x>\d+), Y\+(?P<y>\d+)", puzzle_input[i].split(": ")[1])
        b_match = re.match(r"X\+(?P<x>\d+), Y\+(?P<y>\d+)", puzzle_input[i + 1].split(": ")[1])
        prize_match = re.match(r"X=(?P<x>\d+), Y=(?P<y>\d+)", puzzle_input[i + 2].split(": ")[1])

        a = (int(a_match.group('x')), int(a_match.group('y')))
        b = (int(b_match.group('x')), int(b_match.group('y')))
        prize = (int(prize_match.group('x')), int(prize_match.group('y')))

        yield (a, b, prize)


def get_num_tokens(a: tuple[int, int], b: tuple[int, int], prize: tuple[int, int], part_2: bool) -> int:
    """If it is not possible to win, returns 0."""
    a_x, a_y = a
    b_x, b_y = b
    p_x, p_y = prize

    if part_2:
        p_x += PRIZE_OFFSET
        p_y += PRIZE_OFFSET

    # solve 2x2 system of equations
    matrix_det = a_x * b_y - a_y * b_x
    n_a = (b_y * p_x - b_x * p_y)
    n_b = (a_x * p_y - a_y * p_x)

    # only return if solution is an integer
    if n_a % matrix_det == 0 and n_b % matrix_det == 0:
        if part_2 or (int(n_a / matrix_det) <= MAX_PRESSES and int(n_b / matrix_det) <= MAX_PRESSES):
            return int(n_a / matrix_det) * COST["A"] + int(n_b / matrix_det) * COST["B"]

    return 0


def solve_part_1(puzzle_input: list[str]):
    return sum(get_num_tokens(a, b, prize, False) for (a, b, prize) in parse_input(puzzle_input))


def solve_part_2(puzzle_input: list[str]):
    return sum(get_num_tokens(a, b, prize, True) for (a, b, prize) in parse_input(puzzle_input))


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
