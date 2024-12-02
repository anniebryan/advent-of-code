"""
Advent of Code 2021
Day 16: Packet Decoder
"""

import click
import os
import pathlib


def hex_to_bin(hex_char):
    return bin(int(hex_char, 16))[2:].zfill(4)


def bit_str(hex_str):
    return ''.join([hex_to_bin(char) for char in hex_str])


def get_op(type_id):
    if type_id == 0:  # sum
        op = lambda x, y : x + y
    elif type_id == 1:  # product
        op = lambda x, y: x * y
    elif type_id == 2:  # minimum
        op = lambda x, y: min(x, y)
    elif type_id == 3:  # maximum
        op = lambda x, y: max(x, y)
    elif type_id == 5:  # greater than
        op = lambda x, y: 1 if x > y else 0
    elif type_id == 6:  # less than
        op = lambda x, y: 1 if x < y else 0
    else:  # equal to
        op = lambda x, y: 1 if x == y else 0
    return op


def decode_literal(version, s):
    literal_val = ''
    i = 6
    while s[i] != '0':  # last bit
        literal_val += s[i + 1:i + 5]
        i += 5
    literal_val += s[i + 1:i + 5]
    return version, int(literal_val, 2), s[i + 5:]


def decode_total_length_type(version, s, op):
    total_length = int(s[7:22], 2)
    remaining = s[22:22 + total_length]
    version_sum = version
    accum_val = None
    while remaining:
        version, val, remaining = decode_packet(remaining)
        accum_val = val if accum_val is None else op(accum_val, val)
        version_sum += version
    return version_sum, accum_val, s[22 + total_length:]


def decode_num_subpackets_type(version, s, op):
    num_sub_packets = int(s[7:18], 2)
    remaining = s[18:]
    version_sum = version
    accum_val = None
    for _ in range(num_sub_packets):
        version, val, remaining = decode_packet(remaining)
        accum_val = val if accum_val is None else op(accum_val, val)
        version_sum += version
    return version_sum, accum_val, remaining


def decode_packet(s):
    version = int(s[:3], 2)
    type_id = int(s[3:6], 2)
    if type_id == 4:  # literal
        return decode_literal(version, s)
    else:  # operator
        op = get_op(type_id)
        length_type_id = int(s[6])
        if length_type_id == 0:
            return decode_total_length_type(version, s, op)
        else:
            return decode_num_subpackets_type(version, s, op)


def solve_part_1(puzzle_input: list[str]):
    hex_str = puzzle_input[0]
    return decode_packet(bit_str(hex_str))[0]


def solve_part_2(puzzle_input: list[str]):
    hex_str = puzzle_input[0]
    return decode_packet(bit_str(hex_str))[1]


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
