"""
Advent of Code 2023
Day 4: Scratchcards
"""

import click
import os
from pathlib import Path
import regex as re


def get_num_matches(winning_numbers: set[int], numbers_you_have: set[int]) -> set[int]:
    return len(winning_numbers & numbers_you_have)


def parse_card(line: str) -> tuple[int, set[int], set[int]]:
    pattern = r'Card( *)(?P<card_num>\d+): (?P<winning_numbers>.*) \| (?P<numbers_you_have>.*)'
    match = re.match(pattern, line)
    card_num = int(match.group('card_num'))
    winning_numbers = set([int(n) for n in match.group('winning_numbers').split()])
    numbers_you_have = set([int(n) for n in match.group('numbers_you_have').split()])
    return card_num, winning_numbers, numbers_you_have


def solve_part_1(puzzle_input: list[str]):
    points = []
    for line in puzzle_input:
        _, winning_numbers, numbers_you_have = parse_card(line)
        num_winners = get_num_matches(winning_numbers, numbers_you_have)
        num_points = 0 if num_winners == 0 else 2 ** (num_winners - 1)
        points.append(num_points)
    return sum(points)


def solve_part_2(puzzle_input: list[str]):
    all_card_nums = set()
    for line in puzzle_input:
        card_num, _, _ = parse_card(line)
        all_card_nums.add(card_num)
    copies = {card_num: 1 for card_num in all_card_nums}

    for line in puzzle_input:
        card_num, winning_numbers, numbers_you_have = parse_card(line)
        num_winners = get_num_matches(winning_numbers, numbers_you_have)
        for i in range(num_winners):
            copy_card_num = card_num + i + 1
            if copy_card_num in copies:
                copies[copy_card_num] += copies[card_num]
    
    return sum(copies.values())


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
