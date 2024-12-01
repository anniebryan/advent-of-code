"""
Advent of Code 2021
Day 10: Syntax Scoring
"""

from collections import deque
from statistics import median

TABLE = {')': 3, ']': 57, '}': 1197, '>': 25137}
POINTS = {')': 1, ']': 2, '}': 3, '>': 4}
OPENING_CHARS = {'(', '[', '{', '<'}
CLOSING_CHARS = {'(': ')', '[': ']', '{': '}', '<': '>'}


def find_first_illegal_char(line):
    chars = deque()
    for s in line:
        if s in OPENING_CHARS:
            chars.append(CLOSING_CHARS[s])
        else:
            expected = chars.pop()
            if s != expected:
                return s


def fill_incomplete(line):
    chars = deque()
    for s in line:
        if s in OPENING_CHARS:
            chars.append(CLOSING_CHARS[s])
        else:
            expected = chars.pop()
            if s != expected:
                return None  # corrupted line
    completion_string = ''
    while chars:
        completion_string += chars.pop()
    return completion_string


def get_score(completion_string):
    score = 0
    for s in completion_string:
        score *= 5
        score += POINTS[s]
    return score


def solve_part_1(puzzle_input: list[str]):
    total = 0
    for line in puzzle_input:
        if (char := find_first_illegal_char(line)) is not None:
            total += TABLE[char]
    return total


def solve_part_2(puzzle_input: list[str]):
    scores = []
    for line in puzzle_input:
        if (completion_string := fill_incomplete(line)) is not None:
            scores.append(get_score(completion_string))
    return median(scores)
