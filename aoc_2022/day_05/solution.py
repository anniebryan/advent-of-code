"""
Advent of Code 2022
Day 5: Supply Stacks
"""

import os
from collections import defaultdict
from pathlib import Path

import click
import regex as re


def get_crates_and_instructions(puzzle_input):
    crates = defaultdict(list)
    instructions = []
    is_instruction = False
    for row in puzzle_input:
        if row == "":
            is_instruction = True  # switch
        elif is_instruction:
            items = row.split()
            instructions.append(tuple([int(items[i]) for i in [1, 3, 5]]))
        else:  # crate
            for i, ch in enumerate(row):
                if i % 4 == 1 and ch != ' ' and not re.match('\d+', ch):
                    crates[(i // 4) + 1].append(ch)
    crates = {i: crates[i][::-1] for i in crates}
    return crates, instructions


def execute_instruction(instruction, crates, part_2):
    a, b, c = instruction
    elems = [crates[b].pop() for _ in range(a)]
    if part_2:
        elems = elems[::-1]
    for elem in elems:
        crates[c].append(elem)
    return crates


def execute_instructions(puzzle_input, part_2):
    crates, instructions = get_crates_and_instructions(puzzle_input)
    for instruction in instructions:
        crates = execute_instruction(instruction, crates, part_2)
    return crates


def topmost_crates(crates):
    topmost = [crates[i][-1] for i in sorted(crates.keys())]
    return "".join(topmost)


def solve_part_1(puzzle_input: list[str]):
    crates = execute_instructions(puzzle_input, False)
    return topmost_crates(crates)


def solve_part_2(puzzle_input: list[str]):
    crates = execute_instructions(puzzle_input, True)
    return topmost_crates(crates)


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
