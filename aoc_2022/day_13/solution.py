"""
Advent of Code 2022
Day 13: Distress Signal
"""

import ast
from functools import cmp_to_key


def compare_pair(left, right):
    """
    puzzle_inputs:
        left = a list containing 0 or more integers or other lists
        right = a list containing 0 or more integers or other lists
    Returns:
       -1 if left and right are in the "correct order" (left < right)
        1 if left and right are "out of order"         (left > right)
        0 if left and right are equivalent             (left = right)
    """
    # base case: one or both lists are empty
    if len(left) == 0:
        return 0 if len(right) == 0 else -1
    if len(left) > 0 and len(right) == 0:
        return 1

    left_val = left[0]
    right_val = right[0]

    if isinstance(left_val, int) and isinstance(right_val, int):
        if left_val == right_val:
            return compare_pair(left[1:], right[1:])
        return -1 if left_val < right_val else 1

    if isinstance(left_val, int):
        left_val = [left_val]

    if isinstance(right_val, int):
        right_val = [right_val]

    list_result = compare_pair(left_val, right_val)
    if list_result in {-1, 1}:
        return list_result
    return compare_pair(left[1:], right[1:])


def solve_part_1(puzzle_input):
    pairs = [(ast.literal_eval(puzzle_input[i]), ast.literal_eval(puzzle_input[i + 1])) for i in range(0, len(puzzle_input), 3)]
    in_order_idx_sum = 0
    for i, pair in enumerate(pairs):
        left, right = pair
        if compare_pair(left, right) == -1:
            in_order_idx_sum += i + 1
    return in_order_idx_sum


def solve_part_2(puzzle_input):
    packets = [ast.literal_eval(line) for line in puzzle_input if len(line) > 0]
    divider_packets = ([[2]], [[6]])
    for packet in divider_packets:
        packets.append(packet)

    div_packet_idx_prod = 1
    for i, packet in enumerate(sorted(packets, key=cmp_to_key(compare_pair))):
        if packet in divider_packets:
            div_packet_idx_prod *= (i + 1)
    return div_packet_idx_prod
