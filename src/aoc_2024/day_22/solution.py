"""
Advent of Code 2024
Day 22: Monkey Market
"""

import os
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import click

N_SECRET_NUMS = 2000


def parse_input(puzzle_input: list[str]):
    return [int(n) for n in puzzle_input]


def mix(secret_number: int, res: int) -> int:
    return secret_number ^ res


def prune(secret_number: int) -> int:
    return secret_number % 16777216


def calc_next_secret_number(secret_number: int) -> int:
    secret_number = prune(mix(secret_number, secret_number * 64))
    secret_number = prune(mix(secret_number, int(secret_number / 32)))
    secret_number = prune(mix(secret_number, secret_number * 2048))
    return secret_number


def solve_part_1(puzzle_input: list[str]):
    tot = 0
    for secret_number in parse_input(puzzle_input):
        for _ in range(N_SECRET_NUMS):
            secret_number = calc_next_secret_number(secret_number)
        tot += secret_number
    return tot


def solve_part_2(puzzle_input: list[str]):
    change_to_sales = defaultdict(int)
    for secret_number in parse_input(puzzle_input):
        prices = []
        for _ in range(N_SECRET_NUMS):
            secret_number = calc_next_secret_number(secret_number)
            price = secret_number % 10
            prices.append(price)

        last_4_changes = tuple()
        seen_changes = set()
        for (prev_price, price) in zip(prices, prices[1:]):
            change = price - prev_price
            if len(last_4_changes) == 4:
                last_4_changes = (*last_4_changes[1:], change)
            else:
                last_4_changes = (*last_4_changes, change)

            if len(last_4_changes) == 4 and last_4_changes not in seen_changes:
                seen_changes.add(last_4_changes)
                change_to_sales[last_4_changes] += price

    return max(change_to_sales.values())


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
