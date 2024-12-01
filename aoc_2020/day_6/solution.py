"""
Advent of Code 2020
Day 6: Custom Customs
"""

from collections import defaultdict


def get_all_groups(puzzle_input):
    all_groups = []
    group = []
    for line in puzzle_input:
        if line == "":
            # break between groups
            all_groups.append(group)
            group = []
        else:
            # continuation of current group
            group.extend(line.split())
    all_groups.append(group)
    return all_groups


def get_questions_at_least_one_yes(group):
    return {char for person in group for char in person}


def get_questions_all_yes(group):
    d = defaultdict(int)
    for person in group:
        for char in person:
            d[char] += 1
    return {key for key in d if d[key] == len(group)}


def get_sum_counts(puzzle_input, fn):
    return sum([len(fn(group)) for group in get_all_groups(puzzle_input)])


def solve_part_1(puzzle_input):
    return get_sum_counts(puzzle_input, get_questions_at_least_one_yes)


def solve_part_2(puzzle_input):
    return get_sum_counts(puzzle_input, get_questions_all_yes)
