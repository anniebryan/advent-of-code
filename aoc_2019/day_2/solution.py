"""
Advent of Code 2019
Day 2: 1202 Program Alarm
"""

import click
import os
import pathlib


def get_ints(puzzle_input):
    ints = [int(i) for i in puzzle_input.split(",")]
    return ints


def handle_opcode(i: int, ints: list):
    """
    :param i: index of an opcode
    ints[i] is either 1, 2, or 99
    :return: ints = [2,3,0,3,99]
    >>> handle_opcode(0)
    ints becomes [2,3,0,6,99]
    >>> handle_opcode(4)
    'halt'
    """
    new_ints = ints[:]
    opcode = ints[i]
    if opcode == 99:
        return 'halt'
    else:
        if opcode == 1:
            new_ints[ints[i + 3]] = ints[ints[i + 1]] + ints[ints[i + 2]]
        elif opcode == 2:
            new_ints[ints[i + 3]] = ints[ints[i + 1]] * ints[ints[i + 2]]
        else:
            return 'something went wrong'
        return new_ints


def run_until_halt(ints: list):
    i = 0
    prev_ints, new_ints = ints[:], handle_opcode(i, ints)
    while type(new_ints) is not str:
        prev_ints = new_ints
        i += 4
        new_ints = handle_opcode(i, prev_ints)
    if new_ints == 'halt':
        return prev_ints
    else:
        return 'something went wrong'


def solve_part_1(puzzle_input: list[str]):
    replace = (puzzle_input[0] == "T")
    ints = get_ints(puzzle_input[1])
    if replace:
        ints[1] = 12
        ints[2] = 2
    return run_until_halt(ints)[0]


def solve_part_2(puzzle_input: list[str]):
    replace = (puzzle_input[0] == "T")
    if not replace:
        return "Not supported"
    ints = get_ints(puzzle_input[1])
    desired_output = 19690720
    for noun in range(100):
        for verb in range(100):
            new_ints = ints[:]
            new_ints[1], new_ints[2] = noun, verb
            new_ints = run_until_halt(new_ints)
            if type(new_ints) is not str:
                if new_ints[0] == desired_output:
                    return 100 * noun + verb


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
