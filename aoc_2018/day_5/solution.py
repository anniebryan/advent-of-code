"""
Advent of Code 2018
Day 5: Alchemical Reduction
"""

import string
from functools import reduce


def destroy(p, c):
    # p: previous
    # c: current
    if p is None or len(p) == 0:
        return c
    else:
        l = str(p[-1:])  # last letter
        lc = string.ascii_lowercase
        uc = string.ascii_uppercase
        if (l in lc and c in uc) or (l in uc and c in lc):  # opposite case
            if l.lower() == c.lower():
                return p[:-1]
        return p + c


def solve_part_1(puzzle_input: list[str]):
    s = puzzle_input[0]
    s2 = reduce(destroy, s)
    return len(s2)


def solve_part_2(puzzle_input: list[str]):
    s = puzzle_input[0]
    lengths = {}
    for letter in string.ascii_lowercase:
        s_ = s[:]  # copies to avoid mutating
        s_ = s.replace(letter, '').replace(letter.upper(), '')
        s_ = reduce(destroy, s_)
        lengths[len(s_)] = letter
    num = min(lengths.keys())
    return f"Removing the letter {lengths[num]} yields a string of length {num}"
