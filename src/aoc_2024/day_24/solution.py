"""
Advent of Code 2024
Day 24: Crossed Wires
"""

import os
from collections import deque
from pathlib import Path
from typing import Literal

import click


def parse_input(puzzle_input: list[str]):
    run_part_2 = (puzzle_input[0] == "T")

    wire_values, gates = {}, {}

    second_half = False
    for line in puzzle_input[1:]:
        if line == "":
            second_half = True
        elif second_half:
            [input_1, op, input_2, _, output] = line.split()
            gates[output] = (input_1, op, input_2)
        else:
            wire, val = line.split(": ")
            wire_values[wire] = int(val)

    return wire_values, gates, run_part_2


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


def get_wires_to_swap(gates: dict[set, tuple[str, str, str]]) -> set[str]:
    wires_to_swap = set()
    for output, (input_1, op, input_2) in gates.items():
        if output[0] == "z" and output != max(gates) and op != "XOR":
            wires_to_swap.add(output)
        if op == "XOR":
            if output[0] not in "xyz" and input_1[0] not in "xyz" and input_2[0] not in "xyz":
                wires_to_swap.add(output)
            for (inner_input_1, inner_op, inner_input_2) in gates.values():
                if inner_op == "OR" and (output in {inner_input_1, inner_input_2}):
                    wires_to_swap.add(output)
        if op == "AND" and  input_1 != "x00" and input_2 != "x00":
            for (inner_input_1, inner_op, inner_input_2) in gates.values():
                if inner_op != "OR" and (output in {inner_input_1, inner_input_2}):
                    wires_to_swap.add(output)
    return wires_to_swap


def solve_part_1(puzzle_input: list[str]):
    wire_values, gates, _ = parse_input(puzzle_input)
    wire_values = get_all_wire_values(wire_values, gates)
    return calc_binary(wire_values, "z")


def solve_part_2(puzzle_input: list[str]):
    _, gates, run_part_2 = parse_input(puzzle_input)
    if not run_part_2:
        return
    return ",".join(sorted(get_wires_to_swap(gates)))
