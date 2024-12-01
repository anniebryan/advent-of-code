"""
Advent of Code 2020
Day 1: Report Repair
"""

from collections import defaultdict
from math import prod


def get_expense_report(puzzle_input):
    expense_report = [int(i) for i in puzzle_input]
    return expense_report


def find_two_that_sum(expense_report, n):
    seen = set()
    for i in expense_report:
        if n - i in seen:
            return (i, n - i)
        else:
            seen.add(i)
    return (0, 0)  # no two entries sum to n


def find_three_that_sum(expense_report, n):
    two_way_sums = set()
    two_way_map = defaultdict(set)  # maps sum to set of tuples of indices
    for i in range(len(expense_report)):
        for j in range(i, len(expense_report)):
            s = expense_report[i] + expense_report[j]
            two_way_sums.add(s)
            two_way_map[s].add((i, j))
    for k in range(len(expense_report)):
        missing = n - expense_report[k]
        if missing in two_way_sums:
            for tup in two_way_map[missing]:
                if k not in tup:
                    (i, j) = tup
                    return (expense_report[i], expense_report[j], expense_report[k])
    return (0, 0, 0)  # no three entries sum to n


def solve_part_1(puzzle_input):
    expense_report = get_expense_report(puzzle_input)
    return prod(find_two_that_sum(expense_report, 2020))


def solve_part_2(puzzle_input):
    expense_report = get_expense_report(puzzle_input)
    return prod(find_three_that_sum(expense_report, 2020))
