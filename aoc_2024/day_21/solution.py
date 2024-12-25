"""
Advent of Code 2024
Day 21: Keypad Conundrum
"""

import click
import os
import pathlib
from functools import cache
from itertools import permutations
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


def get_shortest_sequence(code: str) -> str:
    i1, j1 = 3, 2
    ls_1 = []
    for ch in code:
        min_len_1, best_seq_1 = float('inf'), None
        options_1, i1, j1 = get_options(ch, i1, j1, True)
        for o1 in options_1:
            i2, j2 = 0, 2
            ls_2 = []
            for ch_1 in o1:
                min_len_2, best_seq_2 = float('inf'), None
                options_2, i2, j2 = get_options(ch_1, i2, j2, False)
                for o2 in options_2:
                    i3, j3 = 0, 2
                    ls_3 = []
                    for ch_2 in o2:
                        min_len_3, best_seq_3 = float('inf'), None
                        options_3, i3, j3 = get_options(ch_2, i3, j3, False)
                        for o3 in options_3:
                            if len(o3) < min_len_3:
                                min_len_3, best_seq_3 = len(o3), o3
                        ls_3.append(best_seq_3)
                    output_seq_3 = "".join(ls_3)
                    if len(output_seq_3) < min_len_2:
                        min_len_2, best_seq_2 = len(output_seq_3), output_seq_3
                ls_2.append(best_seq_2)
            output_seq_2 = "".join(ls_2)
            if len(output_seq_2) < min_len_1:
                min_len_1, best_seq_1 = len(output_seq_2), output_seq_2
        ls_1.append(best_seq_1)
    return "".join(ls_1)


def solve_part_1(puzzle_input: list[str]):
    res = 0
    for code in puzzle_input:
        numeric_value = int("".join([ch for ch in code if ch != "A"]))
        seq = get_shortest_sequence(code)
        res += numeric_value * len(seq)
    return res


def solve_part_2(puzzle_input: list[str]):
    return


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
