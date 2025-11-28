"""
Advent of Code 2024
Day 19: Linen Layout
"""

def parse_input(puzzle_input: list[str]):
    available_patterns = puzzle_input[0].split(", ")
    desired_designs = puzzle_input[2:]
    return available_patterns, desired_designs


def num_ways(design: str, available_patterns: list[str], memo={}) -> int:
    if design in memo:
        return memo[design]

    n = 0
    for p in available_patterns:
        if design == p:
            n += 1
        elif design.startswith(p):
            n += num_ways(design.removeprefix(p), available_patterns, memo)

    memo[design] = n
    return n


def solve_part_1(puzzle_input: list[str]):
    available_patterns, desired_designs = parse_input(puzzle_input)
    return len([d for d in desired_designs if num_ways(d, available_patterns, {}) > 0])


def solve_part_2(puzzle_input: list[str]):
    available_patterns, desired_designs = parse_input(puzzle_input)
    return sum([num_ways(d, available_patterns, {}) for d in desired_designs])
