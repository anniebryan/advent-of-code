"""
Advent of Code 2025
Day 2: Gift Shop
"""


def parse_input(puzzle_input: list[str], part_2: bool):
    line = puzzle_input[0]
    ranges = [[int(x) for x in r.split("-")] for r in line.split(",")]
    return ranges


def is_invalid_id(num: int, part_2: bool) -> bool:
    s = str(num)
    mid = len(s) // 2

    if part_2:
        for size in range(1, mid + 1):
            if len(s) % size != 0:
                continue
            substrings = []
            for i in range(len(s) // size):
                substrings.append(s[i * size : (i + 1) * size])
            if len(set(substrings)) == 1:
                return True
        return False
    else:
        if len(s) % 2 != 0:
            return False
        left = s[:mid]
        right = s[mid:]
        return left == right


def _solve(puzzle_input: list[str], part_2: bool) -> int:
    ranges = parse_input(puzzle_input, False)
    all_invalid_ids = []
    for (a, b) in ranges:
        for x in range(a, b + 1):
            if is_invalid_id(x, part_2):
                all_invalid_ids.append(x)
    return sum(all_invalid_ids)


def solve_part_1(puzzle_input: list[str]):
    return _solve(puzzle_input, False)


def solve_part_2(puzzle_input: list[str]):
    return _solve(puzzle_input, True)
