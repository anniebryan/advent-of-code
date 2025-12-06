"""
Advent of Code 2025
Day 6: Trash Compactor
"""

from collections import defaultdict
from math import prod


def parse_input(puzzle_input: list[str], part_2: bool):
    problems = defaultdict(list)
    if part_2:
        problem_num = 0
        num_cols, num_rows = len(puzzle_input[0]), len(puzzle_input)
        for i in range(num_cols - 1, -1, -1):
            digits, op = [], None
            for j in range(num_rows):
                ch = puzzle_input[j][i]
                if ch.isnumeric():
                    digits.append(int(ch))
                elif ch != " ":
                    op = ch
            if digits:
                num = 0
                for d in digits:
                    num = (num * 10) + d
                problems[problem_num].append(num)
            if op:
                problems[problem_num].append(op)
                problem_num += 1
    else:
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
