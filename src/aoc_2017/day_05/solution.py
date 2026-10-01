"""
Advent of Code 2017
Day 5: A Maze of Twisty Trampolines, All Alike
"""


def parse_input(puzzle_input: list[str], part_2: bool):
    return [int(n) for n in puzzle_input]


def solve_part_1(puzzle_input: list[str]):
    instructions = parse_input(puzzle_input, False)
    curr_ix = 0
    num_steps = 0
    while 0 <= curr_ix < len(instructions):
        prev_ix = curr_ix
        curr_ix += instructions[curr_ix]
        num_steps += 1
        instructions[prev_ix] += 1
    return num_steps


def solve_part_2(puzzle_input: list[str]):
    instructions = parse_input(puzzle_input, True)
    curr_ix = 0
    num_steps = 0
    while 0 <= curr_ix < len(instructions):
        prev_ix = curr_ix
        offset = instructions[curr_ix]
        curr_ix += offset
        num_steps += 1
        if offset >= 3:
            instructions[prev_ix] -= 1
        else:
            instructions[prev_ix] += 1
    return num_steps
