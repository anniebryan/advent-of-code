"""
Advent of Code 2022
Day 6: Tuning Trouble
"""

def all_different(last_elems):
    return len(last_elems) == len(set(last_elems))


def find_marker(puzzle_input, n):
    puzzle_input = puzzle_input[0]
    last_n = tuple(puzzle_input[:n])
    for i, ch in enumerate(puzzle_input[n:]):
        if all_different(last_n):
            return i + n
        else:
            last_n = last_n[1:] + (ch,)


def solve_part_1(puzzle_input):
    return find_marker(puzzle_input, 4)


def solve_part_2(puzzle_input):
    return find_marker(puzzle_input, 14)
