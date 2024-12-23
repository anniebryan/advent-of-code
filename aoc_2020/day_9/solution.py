"""
Advent of Code 2020
Day 9: Encoding Error
"""

import click
import os
import pathlib
from collections import deque


def get_numbers(puzzle_input):
    numbers = [int(n) for n in puzzle_input]
    return numbers


def init_preamble(numbers, consider_prev):
    last_numbers = deque()
    for i in range(consider_prev):
        last_numbers.append(numbers[i])
    return last_numbers, numbers[consider_prev:]


def exists_sum(last_numbers, n):
    seen = set()
    for i in last_numbers:
        if n - i in seen:
            return True
        else:
            seen.add(i)
    return False


def find_first_invalid(numbers, consider_prev):
    last_numbers, remaining = init_preamble(numbers, consider_prev)
    while exists_sum(last_numbers, remaining[0]):
        last_numbers.popleft()
        last_numbers.append(remaining[0])
        remaining = remaining[1:]
    return remaining[0]


def contiguous_sequence(numbers, target):
    sequence = deque()
    current_sum = 0
    i = 0
    while current_sum != target:
        if current_sum < target:
            n = numbers[i]
            i += 1
            sequence.append(n)
            current_sum += n
        else:  # current sum > target
            n = sequence.popleft()
            current_sum -= n
    return sequence


def encryption_weakness(numbers, target):
    sequence = contiguous_sequence(numbers, target)
    return max(sequence) + min(sequence)


def solve_part_1(puzzle_input: list[str]):
    preamble = int(puzzle_input[0].split("=")[1])
    numbers = get_numbers(puzzle_input[1:])
    return find_first_invalid(numbers, preamble)


def solve_part_2(puzzle_input: list[str]):
    numbers = get_numbers(puzzle_input[1:])
    return encryption_weakness(numbers, solve_part_1(puzzle_input))


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
