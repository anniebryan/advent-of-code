"""
Advent of Code 2018
Day 2: Inventory Management System
"""

import string

def part_1(puzzle_input):
    num_2 = 0
    num_3 = 0
    for box in puzzle_input:
        counts = []
        for letter in string.ascii_lowercase:
            count = box.count(letter)
            counts.append(count)
        if 2 in counts:
            num_2 += 1
        if 3 in counts:
            num_3 += 1
    return num_2*num_3


def part_2(puzzle_input):
    for i in range(len(puzzle_input)):
        box1 = puzzle_input[i]
        remaining = puzzle_input[i+1:]
        for j in range(len(remaining)):
            box2 = remaining[j]
            different = 0
            for l in range(len(box1)-1): # all 27 letters
                if box1[l]!=box2[l]:
                    different += 1
                    letter = l
            if different == 1:
                return box1[0:letter]+box1[letter+1:]
