"""
Advent of Code 2017
Day 10: Knot Hash
"""

from itertools import cycle


def parse_input(puzzle_input: list[str]) -> tuple[int, str]:
    list_size = int(puzzle_input[0])
    input_key = str(puzzle_input[1])
    return list_size, input_key


def get_input_lengths(input_key: str, part_2: bool) -> list[int]:
    if part_2:
        input_lengths = [ord(n) for n in input_key] + [17, 31, 73, 47, 23]
    else:
        input_lengths = [int(n) for n in input_key.split(",")]
    return input_lengths


def _run_one_round(
    c: cycle,
    list_size: int,
    start_ix: int,
    skip_size: int,
    input_lengths: list[int],
) -> tuple[cycle, int, int]:
    for length in input_lengths:
        if length > list_size:
            continue
        values_to_reverse = []
        for _ in range(length):
            values_to_reverse.append(next(c))

        remaining_values = []
        for _ in range(list_size - length):
            remaining_values.append(next(c))

        c = cycle(remaining_values + values_to_reverse[::-1])

        start_ix = (start_ix - length - skip_size) % list_size
        for _ in range(skip_size):
            _ = next(c)
        skip_size += 1

    return c, start_ix, skip_size


def solve_part_1(puzzle_input: list[str]):
    list_size, input_key = parse_input(puzzle_input)
    input_lengths = get_input_lengths(input_key, False)

    c = cycle(range(list_size))

    c, start_ix, _ = _run_one_round(c, list_size, 0, 0, input_lengths)

    for _ in range(start_ix):
        _ = next(c)

    first_val = next(c)
    second_val = next(c)
    return first_val * second_val


def calc_knot_hash(input_key: str, list_size: int = 256) -> str:
    input_lengths = get_input_lengths(input_key, True)

    c = cycle(range(list_size))
    start_ix = 0
    skip_size = 0

    for _ in range(64):
        c, start_ix, skip_size = _run_one_round(c, list_size, start_ix, skip_size, input_lengths)

    if list_size != 256:
        return "N/A"

    sparse_hash = []
    for _ in range(start_ix):
        _ = next(c)
    for _ in range(list_size):
        sparse_hash.append(next(c))

    dense_hash = []
    ix = 0
    for _ in range(16):
        for i in range(16):
            if i == 0:
                xor_value = sparse_hash[ix]
            else:
                xor_value ^= sparse_hash[ix]
            ix += 1
        dense_hash.append(xor_value)

    output_hash = "".join([f"{elem:02x}" for elem in dense_hash])
    return output_hash


def solve_part_2(puzzle_input: list[str]):
    list_size, input_key = parse_input(puzzle_input)
    return calc_knot_hash(input_key, list_size)
