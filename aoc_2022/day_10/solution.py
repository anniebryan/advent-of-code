"""
Advent of Code 2022
Day 10: Cathode-Ray Tube
"""

import click
import os
import pathlib
import regex as re


def execute_program(puzzle_input):
    register = 1
    cycle = 0
    prev_cycle_instr = None
    for row in puzzle_input:
        ready = False
        while not ready:
            # initiate a new cycle
            cycle += 1

            # yield cycle number and register value
            yield cycle, register

            # add value to register
            if prev_cycle_instr is not None:
                register += prev_cycle_instr
                prev_cycle_instr = None
            else:
                ready = True

        # parse a new row's instruction
        if re.match("addx -?(\d+)", row):
            prev_cycle_instr = int(row.split(" ")[1])
        elif row == "noop":
            prev_cycle_instr = None
        else:
            print(f"Cannot parse instruction: {row}")
        

def solve_part_1(puzzle_input: list[str]):
    cycles_of_interest = {20, 60, 100, 140, 180, 220}
    total = 0
    for cycle, register in execute_program(puzzle_input):
        if cycle in cycles_of_interest:
            total += cycle * register
    return total


def solve_part_2(puzzle_input: list[str]):
    s = ["\n"]
    for cycle, register in execute_program(puzzle_input):
        sprite = {register - 1, register, register + 1}
        ix = (cycle - 1) % 40
        if ix in sprite:
            s.append("#")
        else:
            s.append(".")
        if cycle % 40 == 0:
            s.append("\n")
    return "".join(s)


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
