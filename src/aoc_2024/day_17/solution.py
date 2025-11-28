"""
Advent of Code 2024
Day 17: Chronospatial Computer
"""

import os
from pathlib import Path

import click
import regex as re


def parse_input(puzzle_input: list[str]):
    run_part_2 = puzzle_input[0] == "T"
    reg_a = int(re.match(r"Register A: (?P<a>\d+)", puzzle_input[1]).group('a'))
    reg_b = int(re.match(r"Register B: (?P<b>\d+)", puzzle_input[2]).group('b'))
    reg_c = int(re.match(r"Register C: (?P<c>\d+)", puzzle_input[3]).group('c'))
    prog = [int(d) for d in re.match(r"Program: (?P<program>.*)", puzzle_input[5]).group('program').split(",")]
    return run_part_2, reg_a, reg_b, reg_c, prog


def combo(operand: int, reg_a: int, reg_b: int, reg_c: int) -> int:
    if 0 <= operand <= 3:
        return operand
    if operand == 4:
        return reg_a
    if operand == 5:
        return reg_b
    if operand == 6:
        return reg_c
    raise ValueError(f"Unexpected {operand=}")


def execute_instruction(reg_a, reg_b, reg_c, i, opcode, operand):
    inst_pointer = i + 2
    output = None

    if opcode == 0:  # adv
        reg_a = int(reg_a / (2 ** combo(operand, reg_a, reg_b, reg_c)))
    elif opcode == 1:  # bxl
        reg_b = reg_b ^ operand
    elif opcode == 2:  # bst
        reg_b = combo(operand, reg_a, reg_b, reg_c) % 8
    elif opcode == 3:  # jnz
        if reg_a != 0:
            inst_pointer = operand
    elif opcode == 4:  # bxc
        reg_b = reg_b ^ reg_c
    elif opcode == 5:  # out
        output = combo(operand, reg_a, reg_b, reg_c) % 8
    elif opcode == 6:  # bdv
        reg_b = int(reg_a / (2 ** combo(operand, reg_a, reg_b, reg_c)))
    elif opcode == 7:  # cdv
        reg_c = int(reg_a / (2 ** combo(operand, reg_a, reg_b, reg_c)))
    else:
        raise ValueError(f"Unexpected {opcode=}")

    return reg_a, reg_b, reg_c, inst_pointer, output


def run_program(reg_a: int, reg_b: int, reg_c: int, prog: list[int]) -> list[int]:
    all_outputs = []
    i = 0
    while i < len(prog):
        reg_a, reg_b, reg_c, i, output = execute_instruction(reg_a, reg_b, reg_c, i, prog[i], prog[i + 1])
        if output is not None:
            all_outputs.append(output)
    return all_outputs


def min_reg_a(reg_a, reg_b, reg_c, prog, prog_ix):
    if prog_ix < 0:
        return reg_a

    for digit in range(8):
        cand_reg_a = reg_a * 8 | digit
        i = 0
        while i < len(prog):
            cand_reg_a, reg_b, reg_c, i, output = execute_instruction(cand_reg_a, reg_b, reg_c, i, prog[i], prog[i + 1])
            if output is not None:
                break

        if prog[prog_ix] == output:
            if (res := min_reg_a(reg_a * 8 | digit, reg_a, reg_b, prog, prog_ix - 1)) is not None:
                return res

    return None


def solve_part_1(puzzle_input: list[str]):
    _, reg_a, reg_b, reg_c, prog = parse_input(puzzle_input)
    return ",".join([str(o) for o in run_program(reg_a, reg_b, reg_c, prog)])


def solve_part_2(puzzle_input: list[str]):
    run_part_2, _, reg_b, reg_c, prog = parse_input(puzzle_input)
    if not run_part_2:
        return
    return min_reg_a(0, reg_b, reg_c, prog, len(prog) - 1)
