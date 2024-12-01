"""
Advent of Code 2020
Day 10: Adapter Array
"""

from collections import defaultdict
from math import prod


def get_numbers(puzzle_input):
    numbers = [int(n) for n in puzzle_input]
    return numbers


def get_differences(numbers):
    numbers = sorted(numbers + [0, max(numbers) + 3])
    d = defaultdict(int)
    for i in range(len(numbers) - 1):
        d[numbers[i + 1] - numbers[i]] += 1
    return d[1], d[3]


def num_arrangements(numbers, last, memo={}):
    n = len(numbers)
    if n in {0, 1}:
        return 1
    if (n, last) not in memo:
        ways = 0
        i = 0
        while i < len(numbers) and numbers[i] <= last + 3:
            ways += num_arrangements(numbers[i + 1:], numbers[i])
            i += 1
        memo[(n, last)] = ways
    return memo[(n, last)]


def part_1(puzzle_input):
    numbers = get_numbers(puzzle_input)
    return prod(get_differences(numbers))


def part_2(puzzle_input):
    numbers = get_numbers(puzzle_input)
    return num_arrangements(sorted(numbers), 0)
