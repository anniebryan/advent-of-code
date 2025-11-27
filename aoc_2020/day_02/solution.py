"""
Advent of Code 2020
Day 2: Password Philosophy
"""

import click
import os
from pathlib import Path


def get_passwords(puzzle_input):
    passwords = []
    for line in puzzle_input:
        info = line.split()
        low, high = info[0].split("-")
        char = info[1][0]
        password = info[2]
        passwords.append((int(low), int(high), char, password))
    return passwords


def get_password_char_count(password, c):
    count = 0
    for char in password:
        if char == c:
            count += 1
    return count


def get_chars_at(password, i, j):
    return {password[i - 1], password[j - 1]}


def count_valid_passwords(puzzle_input, policy_one):
    """
    policy one: a password is valid if the number of times the given
    character appears is between low and high inclusive
    
    policy two: a password is valid if the given character appears
    exactly once out of the two indices provided (one-indexed)
    """
    num_valid_passwords = 0
    passwords = get_passwords(puzzle_input)
    for password in passwords:
        i, j, c, p = password
        if policy_one:
            if i <= get_password_char_count(p, c) <= j:
                num_valid_passwords += 1
        else:
            chars = get_chars_at(p, i, j)
            if c in chars and len(chars) == 2:
                num_valid_passwords += 1
    return num_valid_passwords


def solve_part_1(puzzle_input: list[str]):
    return count_valid_passwords(puzzle_input, True)


def solve_part_2(puzzle_input: list[str]):
    return count_valid_passwords(puzzle_input, False)


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
