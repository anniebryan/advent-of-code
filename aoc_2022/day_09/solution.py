"""
Advent of Code 2022
Day 9: Rope Bridge
"""

import click
import os
from pathlib import Path


def get_moves(puzzle_input):
    moves = []
    for row in puzzle_input:
        direction, num = row.split(" ")
        for _ in range(int(num)):
            moves.append(direction)
    return moves


def move_head(head, move):
    new_x = head[0] + {"R": 1, "L": -1, "U": 0, "D": 0}[move]
    new_y = head[1] + {"R": 0, "L": 0, "U": 1, "D": -1}[move]
    return (new_x, new_y)


def sign(n):
    return 0 if n == 0 else int(n / abs(n))


def move_tail(head, tail):
    head_x, head_y = head
    tail_x, tail_y = tail

    diff_x = head_x - tail_x
    diff_y = head_y - tail_y

    if -1 <= diff_x <= 1 and -1 <= diff_y <= 1:
        return tail  # already touching, don't need to move
    return (tail_x + sign(diff_x), tail_y + sign(diff_y))


def execute_moves(moves, num_tails):
    head = (0, 0)
    tails = {i + 1: (0, 0) for i in range(num_tails)}
    tail_locations = {tails[num_tails]}
    for move in moves:
        head = move_head(head, move)
        tails[1] = move_tail(head, tails[1])
        for i in range(1, num_tails):
            tails[i + 1] = move_tail(tails[i], tails[i + 1])
        tail_locations.add(tails[num_tails])
    return tail_locations


def solve_part_1(puzzle_input: list[str]):
    moves = get_moves(puzzle_input)
    return len(execute_moves(moves, 1))


def solve_part_2(puzzle_input: list[str]):
    moves = get_moves(puzzle_input)
    return len(execute_moves(moves, 9))


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
