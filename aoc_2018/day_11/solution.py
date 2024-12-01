"""
Advent of Code 2018
Day 11: Chronal Charge
"""

import numpy as np


def get_serial_number(puzzle_input):
    serial_number = int(puzzle_input[0])
    return serial_number


def get_power_level(x, y, serial_number):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    hundreds_digit = (power_level // 100) % 10
    return hundreds_digit - 5


def get_total_power(top_left_x, top_left_y, size, serial_number):
    total_power = 0
    for i in range(size):
        for j in range(size):
            x = top_left_x + i
            y = top_left_y + j
            total_power += get_power_level(x, y, serial_number)
    return total_power


def find_largest_total_power(size, serial_number):
    max_power = get_total_power(0, 0, size, serial_number)
    best_i, best_j = 0, 0
    for i in range(300 - size):
        for j in range(300 - size):
            total_power = get_total_power(i, j, size, serial_number)
            if total_power > max_power:
                max_power = total_power
                best_i, best_j = i, j
    return best_i, best_j


def consider_all_sizes(serial_number):
    powers = np.fromfunction(lambda i, j: get_power_level(i, j, serial_number), (300, 300))
    best_size, max_power, best_x, best_y = 0, 0, 0, 0
    for size in range(1, 300):
        boxes = sum([powers[x:x - size, y:y - size] for x in range(size) for y in range(size)])
        power = int(boxes.max())
        if power > max_power:
            max_power = power
            best_size = size
            best_x, best_y = np.where(boxes == max_power)
    return int(best_x[0]), int(best_y[0]), best_size


def solve_part_1(puzzle_input):
    serial_number = get_serial_number(puzzle_input)
    return find_largest_total_power(3, serial_number)


def solve_part_2(puzzle_input):
    serial_number = get_serial_number(puzzle_input)
    return consider_all_sizes(serial_number)
