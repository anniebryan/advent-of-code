"""
Advent of Code 2023
Day 7: Camel Cards
"""

import os
from collections import Counter
from functools import cmp_to_key
from pathlib import Path

import click


def parse_input(puzzle_input: list[str]):
    hands = []
    for line in puzzle_input:
        hand, bid = line.split()
        hands.append(([c for c in hand], int(bid)))
    return hands


def get_type(cards: Counter) -> int:
    """
    Return an integer between 0-6 (inclusive), corresponding to the hand's type.
    Higher values correspond to better types.
    """
    if len(cards) == 1:  # 5 of a kind
        return 6
    if len(cards) == 2:
        if 4 in cards.values():  # 4 of a kind
            return 5
        else:  # full house
            return 4
    if 3 in cards.values():  # 3 of a kind
        return 3
    if Counter(cards.values()) == {2: 2, 1: 1}:  # 2 pair
        return 2
    if Counter(cards.values()) == {2: 1, 1: 3}:  # 1 pair
        return 1
    return 0


def get_best_type(cards: Counter) -> int:
    if "J" not in cards:
        return get_type(cards)
    num_j = cards["J"]
    if len(cards) in {1, 2}:  # 5 of a kind
        return 6
    if len(cards) == 3:
        if (4 - num_j) in cards.values():  # 4 of a kind
            return 5
        if (3 - num_j) in cards.values():  # full house
            return 4
        if (2 - num_j) in cards.values():  # full house
            return 4
    if len(cards) == 4:
        if (3 - num_j) in cards.values():  # 3 of a kind
            return 3
        if (2 - num_j) in cards.values():  # 2 pair
            return 2
    if len(cards) == 5:  # 1 pair
        return 1
    return 0


def compare_hands(hand_1, hand_2, type_fn, card_values) -> int:

    cards_1, cards_2 = hand_1[0], hand_2[0]
    counter_1, counter_2 = Counter(cards_1), Counter(cards_2)

    type_1, type_2 = type_fn(counter_1), type_fn(counter_2)
    if type_1 != type_2:
        return type_1 - type_2

    for i in range(5):
        if cards_1[i] != cards_2[i]:
            return card_values[cards_1[i]] - card_values[cards_2[i]]

    raise ValueError(f"Could not determine order between {cards_1} and {cards_2}")


def calc_total_winnings(hands, key) -> int:
    total_winnings = 0
    for i, (_, bid) in enumerate(sorted(hands, key=key)):
        total_winnings += bid * (i + 1)
    return total_winnings


def solve_part_1(puzzle_input: list[str]):
    hands = parse_input(puzzle_input)
    card_values = {ch: ix for ix, ch in enumerate("23456789TJQKA")}
    key = cmp_to_key(lambda x, y: compare_hands(x, y, get_type, card_values))
    return calc_total_winnings(hands, key)


def solve_part_2(puzzle_input: list[str]):
    hands = parse_input(puzzle_input)
    card_values = {ch: ix for ix, ch in enumerate("J23456789TQKA")}
    key = cmp_to_key(lambda x, y: compare_hands(x, y, get_best_type, card_values))
    return calc_total_winnings(hands, key)


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
