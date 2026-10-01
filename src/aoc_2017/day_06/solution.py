"""
Advent of Code 2017
Day 6: Memory Reallocation
"""


def parse_input(puzzle_input: list[str], part_2: bool):
    return [int(n) for n in puzzle_input[0].split()]


def solve_part_1(puzzle_input: list[str]):
    banks = parse_input(puzzle_input, False)
    seen = set()
    num_cycles = 0
    state = " ".join(str(b) for b in banks)
    while state not in seen:
        seen.add(state)
        curr_ix, largest_bank = max(enumerate(banks), key=lambda t: t[1])
        banks[curr_ix] = 0
        for _ in range(largest_bank):
            curr_ix += 1
            curr_ix %= len(banks)
            banks[curr_ix] += 1
        num_cycles += 1
        state = " ".join(str(b) for b in banks)
    return num_cycles


def solve_part_2(puzzle_input: list[str]):
    banks = parse_input(puzzle_input, True)
    seen = {}
    num_cycles = 0
    state = " ".join(str(b) for b in banks)
    while state not in seen:
        seen[state] = num_cycles
        curr_ix, largest_bank = max(enumerate(banks), key=lambda t: t[1])
        banks[curr_ix] = 0
        for _ in range(largest_bank):
            curr_ix += 1
            curr_ix %= len(banks)
            banks[curr_ix] += 1
        num_cycles += 1
        state = " ".join(str(b) for b in banks)
    return num_cycles - seen[state]
