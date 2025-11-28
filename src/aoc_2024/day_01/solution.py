"""
Advent of Code 2024
Day 1: Historian Hysteria
"""

import os
from collections import Counter
from pathlib import Path

import click
import regex as re


def parse_input(puzzle_input):
    left_list, right_list = [], []
    for line in puzzle_input:
        nums = re.findall('\d+', line)
        assert len(nums) == 2
        left_num, right_num = nums
        left_list.append(int(left_num))
        right_list.append(int(right_num))
    return sorted(left_list), sorted(right_list)


def solve_part_1(puzzle_input):
    left_list, right_list = parse_input(puzzle_input)
    all_distances = []
    for x, y in zip(left_list, right_list):
        all_distances.append(abs(x - y))
    return sum(all_distances)


def solve_part_2(puzzle_input):
    left_list, right_list = parse_input(puzzle_input)
    right_occurrences = Counter(right_list)
    all_distances = []
    for x in left_list:
        all_distances.append(x * right_occurrences[x])
    return sum(all_distances)
