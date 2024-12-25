"""
Advent of Code 2024
Day 21: Keypad Conundrum
"""

import click
import os
import pathlib
from functools import cache
from itertools import permutations
from typing import Callable
from utils import Grid


NUMERIC_KEYPAD = Grid(["789", "456", "123", ".0A"])
DIRECTIONAL_KEYPAD = Grid([".^A", "<v>"])


@cache
def p_is_valid(p: tuple[str], i: int, j: int, is_numeric_keypad: bool) -> bool:
    keypad = NUMERIC_KEYPAD if is_numeric_keypad else DIRECTIONAL_KEYPAD
    for move in p:
        di, dj = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}[move]
        i += di
        j += dj
        if keypad.at(i, j) == ".":
            return False
    return True


@cache
def get_options(ch: str, start_i: int, start_j: int, is_numeric_keypad: bool) -> tuple[set[str], int, int]:
    keypad = NUMERIC_KEYPAD if is_numeric_keypad else DIRECTIONAL_KEYPAD
    dest_i, dest_j = keypad.where(ch)[0]
    s = []

    if dest_i > start_i:
        for _ in range(dest_i - start_i):
            s.append("v")
    else:
        for _ in range(start_i - dest_i):
            s.append("^")

    if dest_j > start_j:
        for _ in range(dest_j - start_j):
            s.append(">")
    else:
        for _ in range(start_j - dest_j):
            s.append("<")

    options = set()
    for p in permutations(s):
        if p_is_valid(p, start_i, start_j, is_numeric_keypad):
            options.add("".join(p) + "A")
    return options, dest_i, dest_j


@cache
def get_shortest_sequence(code: str, i: int, j: int, is_numeric_keypad: bool, num_directional_keypads: int) -> str:
    ls = []
    for ch in code:
        min_len, best_seq = float("inf"), None
        options, i, j = get_options(ch, i, j, is_numeric_keypad)
        for o in options:
            if is_numeric_keypad:
                output_seq = get_shortest_sequence(o, 0, 2, False, num_directional_keypads)
            elif num_directional_keypads > 1:
                output_seq = get_shortest_sequence(o, 0, 2, False, num_directional_keypads - 1)
            else:
                output_seq = o
            if len(output_seq) < min_len:
                min_len, best_seq = len(output_seq), output_seq
        ls.append(best_seq)
    return "".join(ls)


def get_total_complexity(puzzle_input: list[str], num_directional_keypads: int):
    res = 0
    for code in puzzle_input:
        numeric_value = int("".join([ch for ch in code if ch != "A"]))
        seq = get_shortest_sequence(code, 3, 2, True, num_directional_keypads)
        res += numeric_value * len(seq)
    return res


def solve_part_1(puzzle_input: list[str]):
    return get_total_complexity(puzzle_input, 2)


# TODO speedup
def solve_part_2(puzzle_input: list[str]):
    return get_total_complexity(puzzle_input, 25)


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
