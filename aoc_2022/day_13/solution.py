"""
Advent of Code 2022
Day 13: Distress Signal
"""

import click
import os
from pathlib import Path
import ast
from functools import cmp_to_key


def compare_pair(left, right):
    """
    puzzle_inputs:
        left = a list containing 0 or more integers or other lists
        right = a list containing 0 or more integers or other lists
    Returns:
       -1 if left and right are in the "correct order" (left < right)
        1 if left and right are "out of order"         (left > right)
        0 if left and right are equivalent             (left = right)
    """
    # base case: one or both lists are empty
    if len(left) == 0:
        return 0 if len(right) == 0 else -1
    if len(left) > 0 and len(right) == 0:
        return 1

    left_val = left[0]
    right_val = right[0]

    if isinstance(left_val, int) and isinstance(right_val, int):
        if left_val == right_val:
            return compare_pair(left[1:], right[1:])
        return -1 if left_val < right_val else 1

    if isinstance(left_val, int):
        left_val = [left_val]

    if isinstance(right_val, int):
        right_val = [right_val]

    list_result = compare_pair(left_val, right_val)
    if list_result in {-1, 1}:
        return list_result
    return compare_pair(left[1:], right[1:])


def solve_part_1(puzzle_input: list[str]):
    pairs = [(ast.literal_eval(puzzle_input[i]), ast.literal_eval(puzzle_input[i + 1])) for i in range(0, len(puzzle_input), 3)]
    in_order_idx_sum = 0
    for i, pair in enumerate(pairs):
        left, right = pair
        if compare_pair(left, right) == -1:
            in_order_idx_sum += i + 1
    return in_order_idx_sum


def solve_part_2(puzzle_input: list[str]):
    packets = [ast.literal_eval(line) for line in puzzle_input if len(line) > 0]
    divider_packets = ([[2]], [[6]])
    for packet in divider_packets:
        packets.append(packet)

    div_packet_idx_prod = 1
    for i, packet in enumerate(sorted(packets, key=cmp_to_key(compare_pair))):
        if packet in divider_packets:
            div_packet_idx_prod *= (i + 1)
    return div_packet_idx_prod


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
