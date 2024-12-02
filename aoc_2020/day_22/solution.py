"""
Advent of Code 2020
Day 22: Crab Combat
"""

import click
import os
import pathlib
from collections import deque


def get_initial_decks(puzzle_input):
    p1, p2 = deque(), deque()
    current_player = None
    for row in puzzle_input:
        if "Player" in row:
            current_player = int(row.split()[1][:-1])
        elif row != "":
            if current_player == 1:
                p1.append(int(row))
            elif current_player == 2:
                p2.append(int(row))
    return p1, p2


def play_round(p1, p2):
    p1_card = p1.popleft()
    p2_card = p2.popleft()
    if p1_card > p2_card:
        p1.extend([p1_card, p2_card])
    else:
        p2.extend([p2_card, p1_card])
    return p1, p2


def to_str(p1, p2):
    p1_str = "".join(str(card) for card in p1)
    p2_str = "".join(str(card) for card in p2)
    return f"{p1_str}-{p2_str}"


def get_new_deques(p1, p1_card, p2, p2_card):
    new_p1 = deque()
    for i in range(p1_card):
        new_p1.append(p1[i])
    new_p2 = deque()
    for i in range(p2_card):
        new_p2.append(p2[i])
    return new_p1, new_p2


def play_recursive_round(p1, p2, seen):
    if to_str(p1, p2) in seen:
        while p2:
            p1.append(p2.pop())
        return p1, p2, seen
    else:
        seen.add(to_str(p1, p2))
    p1_card = p1.popleft()
    p2_card = p2.popleft()
    if len(p1) >= p1_card and len(p2) >= p2_card:
        new_p1, new_p2 = get_new_deques(p1, p1_card, p2, p2_card)
        score_1, score_2 = play_recursive_game(new_p1, new_p2)
        if score_1 > score_2:
            p1.extend([p1_card, p2_card])
        else:
            p2.extend([p2_card, p1_card])
    else:
        if p1_card > p2_card:
            p1.extend([p1_card, p2_card])
        else:
            p2.extend([p2_card, p1_card])
    return p1, p2, seen


def score(queue):
    s, i = 0, 1
    while queue:
        s += i * queue.pop()
        i += 1
    return s


def play_game(p1, p2):
    while len(p1) > 0 and len(p2) > 0:
        p1, p2 = play_round(p1, p2)
    return score(p1), score(p2)


def play_recursive_game(p1, p2):
    seen = set()
    while len(p1) > 0 and len(p2) > 0:
        p1, p2, seen = play_recursive_round(p1, p2, seen)
    return score(p1), score(p2)


def solve_part_1(puzzle_input: list[str]):
    p1, p2 = get_initial_decks(puzzle_input)
    return max(play_game(p1, p2))


def solve_part_2(puzzle_input: list[str]):
    p1, p2 = get_initial_decks(puzzle_input)
    return max(play_recursive_game(p1, p2))


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
