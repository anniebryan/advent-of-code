"""
Advent of Code 2024
Day 24: Crossed Wires
"""

import click
import os
import pathlib
from typing import Literal
from collections import deque


def parse_input(puzzle_input: list[str]):
    run_part_2 = (puzzle_input[0] == "T")
    num_swaps = int(puzzle_input[1])

    wire_values = {}
    gates = {}

    second_half = False
    for line in puzzle_input[2:]:
        if line == "":
            second_half = True
        elif second_half:
            [input_1, op, input_2, _, output] = line.split()
            gates[output] = (input_1, op, input_2)
        else:
            wire, val = line.split(": ")
            wire_values[wire] = int(val)

    return wire_values, gates, run_part_2, num_swaps


def calc_output(input_1: Literal[0, 1], op: Literal["AND", "OR", "XOR"], input_2: Literal[0, 1]) -> int:
    if op == "AND":
        return input_1 & input_2
    if op == "OR":
        return input_1 | input_2
    if op == "XOR":
        return input_1 ^ input_2
    raise ValueError(f"Invalid {op=}")


def calc_binary(wire_values: dict[str, int], first_ch: str) -> int:
    res = 0
    for wire, val in wire_values.items():
        if wire[0] == first_ch:
            wire_bit = int(wire[1:])
            res += val * (2 ** wire_bit)
    return res


def get_all_wire_values(wire_values: dict[str, int], gates: dict[str, tuple[str, str, str]]):
    q = deque()
    for g in gates.keys():
        q.append(g)

    while q:
        g = q.popleft()
        (input_1, op, input_2) = gates[g]
        if input_1 in wire_values and input_2 in wire_values:
            wire_values[g] = calc_output(wire_values[input_1], op, wire_values[input_2])
        else:
            q.append(g)
    return wire_values


def get_wires_to_swap(wire_values: dict[str, int],
                      gates: dict[set, tuple[str, str, str]],
                      num_swaps: int) -> set[str]:
    raise NotImplementedError  # TODO


def solve_part_1(puzzle_input: list[str]):
    wire_values, gates, _, _ = parse_input(puzzle_input)
    wire_values = get_all_wire_values(wire_values, gates)
    return calc_binary(wire_values, "z")


def solve_part_2(puzzle_input: list[str]):
    wire_values, gates, run_part_2, num_swaps = parse_input(puzzle_input)
    if not run_part_2:
        return
    wire_values = get_all_wire_values(wire_values, gates)
    return ",".join(sorted(get_wires_to_swap(wire_values, gates, num_swaps)))


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
