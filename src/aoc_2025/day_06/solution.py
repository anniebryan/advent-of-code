"""
Advent of Code 2025
Day 6: Trash Compactor
"""

from collections import defaultdict
from math import prod


def parse_input(puzzle_input: list[str], part_2: bool):
    if part_2:
        chars = defaultdict(dict)
        for i, line in enumerate(puzzle_input):
            for j, ch in enumerate(line[::-1]):
                if ch.isnumeric():
                    chars[j][i] = int(ch)
                else:
                    chars[j][i] = ch

        i = 0
        problems = defaultdict(list)
        for col in sorted(chars):
            digits, op = [], None
            for _, val in sorted(chars[col].items()):
                if isinstance(val, int):
                    digits.append(val)
                elif val in {"+", "*"}:
                    op = val
                elif val == " ":
                    pass
                else:
                    raise ValueError(f"Unexpected {val=}")
            if digits:
                num = 0
                for d in digits:
                    num *= 10
                    num += d
                problems[i].append(num)
            if op:
                problems[i].append(op)
                i += 1
    else:
        problems = defaultdict(list)
        for line in puzzle_input:
            for i, ch in enumerate(line.strip().split()):
                if ch.isnumeric():
                    problems[i].append(int(ch))
                else:
                    problems[i].append(ch)
    return problems


def _solve(problems: dict[int, list]) -> int:
    tot = 0
    for p in problems.values():
        op = p[-1]
        if op == "*":
            tot += prod(p[:-1])
        elif op == "+":
            tot += sum(p[:-1])
        else:
            raise ValueError(f"Unknown operator: {op}")
    return tot


def solve_part_1(puzzle_input: list[str]):
    problems = parse_input(puzzle_input, False)
    return _solve(problems)


def solve_part_2(puzzle_input: list[str]):
    problems = parse_input(puzzle_input, True)
    return _solve(problems)
