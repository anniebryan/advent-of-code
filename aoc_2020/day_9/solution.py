"""
Advent of Code 2020
Day 9: Encoding Error
"""

from collections import deque


def get_numbers(puzzle_input):
    numbers = [int(n) for n in puzzle_input]
    return numbers


def init_preamble(numbers, consider_prev):
    last_numbers = deque()
    for i in range(consider_prev):
        last_numbers.append(numbers[i])
    return last_numbers, numbers[consider_prev:]


def exists_sum(last_numbers, n):
    seen = set()
    for i in last_numbers:
        if n - i in seen:
            return True
        else:
            seen.add(i)
    return False


def find_first_invalid(numbers, consider_prev):
    last_numbers, remaining = init_preamble(numbers, consider_prev)
    while exists_sum(last_numbers, remaining[0]):
        last_numbers.popleft()
        last_numbers.append(remaining[0])
        remaining = remaining[1:]
    return remaining[0]


def contiguous_sequence(numbers, target):
    sequence = deque()
    current_sum = 0
    i = 0
    while current_sum != target:
        if current_sum < target:
            n = numbers[i]
            i += 1
            sequence.append(n)
            current_sum += n
        else:  # current sum > target
            n = sequence.popleft()
            current_sum -= n
    return sequence


def encryption_weakness(numbers, target):
    sequence = contiguous_sequence(numbers, target)
    return max(sequence) + min(sequence)


def solve_part_1(puzzle_input):
    preamble = int(puzzle_input[0].split("=")[1])
    numbers = get_numbers(puzzle_input[1:])
    return find_first_invalid(numbers, preamble)


def solve_part_2(puzzle_input):
    numbers = get_numbers(puzzle_input[1:])
    return encryption_weakness(numbers, part_1(puzzle_input))
