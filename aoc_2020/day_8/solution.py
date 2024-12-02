"""
Advent of Code 2020
Day 8: Handheld Halting
"""

import click
import os
import pathlib


def get_instructions(puzzle_input):
    instructions = {}
    for i in range(len(puzzle_input)):
        vals = puzzle_input[i].split()
        instructions[i] = (vals[0], int(vals[1]))
    return instructions


def process_instruction(instructions, i, acc, override = None):
    if override is not None and override[0] == i:
        instruction = (override[1], instructions[i][1])
    else:
        instruction = instructions[i]
    next_i = i + instruction[1] if instruction[0] == 'jmp' else i + 1
    new_acc = acc + instruction[1] if instruction[0] == 'acc' else acc
    return next_i, new_acc


def run_sequence(instructions, override = None):
    seen = {0}
    i, acc = 0, 0
    while True:
        i, acc = process_instruction(instructions, i, acc, override)
        if i in seen:  # found cycle
            return (False, acc)
        elif i == len(instructions):  # properly terminated
            return (True, acc)
        else:
            seen.add(i)


def try_all_sequences(instructions):
    for i in instructions:
        if instructions[i][0] == 'nop':  # change to 'jmp'
            override = (i, 'jmp')
            result = run_sequence(instructions, override)
            if result[0]:
                return result[1]
        elif instructions[i][0] == 'jmp':  # change to 'nop'
            override = (i, 'nop')
            result = run_sequence(instructions, override)
            if result[0]:
                return result[1]


def solve_part_1(puzzle_input: list[str]):
    instructions = get_instructions(puzzle_input)
    return run_sequence(instructions)[1]


def solve_part_2(puzzle_input: list[str]):
    instructions = get_instructions(puzzle_input)
    return try_all_sequences(instructions)


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
