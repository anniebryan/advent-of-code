"""
Advent of Code 2018
Day 9: Marble Mania
"""

import click
import os
from pathlib import Path
import regex as re
from collections import deque, defaultdict


def get_info(puzzle_input):
    pattern = r'([\d]+) players; last marble is worth ([\d]+) points'
    num_players, last_marble = map(lambda x: int(x), re.findall(pattern, puzzle_input[0])[0])
    return num_players, last_marble


def take_turn(current_marble_index, marble_to_place, player, circle, scores):
    if marble_to_place % 23 == 0:
        scores[player] += marble_to_place
        index_to_remove = (current_marble_index - 7) % len(circle)
        scores[player] += circle[index_to_remove]
        new_circle = circle[:index_to_remove] + circle[index_to_remove + 1:]
        new_current_marble_index = index_to_remove
    else:
        index_to_add = (current_marble_index + 2) % len(circle)
        new_circle = circle[:index_to_add] + [marble_to_place] + circle[index_to_add:]
        new_current_marble_index = index_to_add
    return new_current_marble_index, new_circle, scores


def run_game(num_players, last_marble):
    scores = defaultdict(int)
    circle = deque([0])

    for marble in range(last_marble):
        if (marble + 1) % 23 == 0:
            circle.rotate(7)
            index_to_remove = (marble + 1) % num_players
            scores[index_to_remove] += marble + 1 + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble + 1)

    return max(scores.values())


def solve_part_1(puzzle_input: list[str]):
    num_players, last_marble = get_info(puzzle_input)
    return run_game(num_players, last_marble)


def solve_part_2(puzzle_input: list[str]):
    num_players, last_marble = get_info(puzzle_input)
    last_marble *= 100
    return run_game(num_players, last_marble)


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
