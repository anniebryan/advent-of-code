"""
Advent of Code 2022
Day 3: Rucksack Reorganization
"""

def letter_in_common(row):
    n = len(row) // 2
    left = set()
    for i in range(len(row)):
        ch = row[i]
        if i < n:
            left.add(ch)
        elif ch in left:
            return ch


def letter_in_common_3(a, b, c):
    a_ch = set([ch for ch in a])
    b_ch = set([ch for ch in b])
    for ch in c:
        if ch in a_ch and ch in b_ch:
            return ch


def priority(ch):
    if 97 <= ord(ch) <= 122:
        return ord(ch) - 96
    return ord(ch) - 38


def part_1(puzzle_input):
    tot = 0
    for row in puzzle_input:
        ch = letter_in_common(row)
        tot += priority(ch)
    return tot


def part_2(puzzle_input):
    tot = 0
    for i in range(0, len(puzzle_input), 3):
        ch = letter_in_common_3(*puzzle_input[i:i + 3])
        tot += priority(ch)
    return tot
