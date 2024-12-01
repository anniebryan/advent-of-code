"""
Advent of Code 2018
Day 2: Inventory Management System
"""

import string


def solve_part_1(puzzle_input):
    num_2, num_3 = 0, 0
    for box in puzzle_input:
        counts = []
        for letter in string.ascii_lowercase:
            count = box.count(letter)
            counts.append(count)
        if 2 in counts:
            num_2 += 1
        if 3 in counts:
            num_3 += 1
    return num_2 * num_3


def solve_part_2(puzzle_input):
    for i in range(len(puzzle_input)):
        box_1 = puzzle_input[i]
        remaining = puzzle_input[i + 1:]
        for j in range(len(remaining)):
            box_2 = remaining[j]
            different = 0
            for l in range(len(box_1) - 1):  # all 27 letters
                if box_1[l] != box_2[l]:
                    different += 1
                    letter = l
            if different == 1:
                return box_1[0:letter] + box_1[letter + 1:]
