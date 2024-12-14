"""
Advent of Code 2023
Day 15: Lens Library
"""

import click
import os
import pathlib
from collections import defaultdict, deque


def parse_input(puzzle_input: list[str]):
    for s in puzzle_input[0].split(","):
        yield s


def run_hash_algorithm(s: str) -> int:
    tot = 0
    for ch in s:
        tot += ord(ch)
        tot *= 17
        tot %= 256
    return tot


def get_all_boxes(puzzle_input: list[str]) -> tuple[dict[int, deque], dict[str, str]]:
    all_labels = set()
    focal_lengths = {}
    boxes = defaultdict(deque)
    for s in parse_input(puzzle_input):
        if "-" in s:
            label = s.split("-")[0]
            box = run_hash_algorithm(label)
            if label in all_labels:
                all_labels.remove(label)
                boxes[box].remove(label)
        else:
            label, focal_len = s.split("=")
            box = run_hash_algorithm(label)
            focal_lengths[label] = focal_len
            if label not in all_labels:
                all_labels.add(label)
                boxes[box].append(label)
    return boxes, focal_lengths


def focusing_power(boxes: dict[int, deque], focal_lengths: dict[str, str]) -> None:
    tot = 0
    for box_num, lenses in boxes.items():
        for i, label in enumerate(lenses):
            tot += (box_num + 1) * (i + 1) * int(focal_lengths[label])
    return tot


def solve_part_1(puzzle_input: list[str]):
    return sum([run_hash_algorithm(s) for s in parse_input(puzzle_input)])


def solve_part_2(puzzle_input: list[str]):
    boxes, focal_lengths = get_all_boxes(puzzle_input)
    return focusing_power(boxes, focal_lengths)


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
