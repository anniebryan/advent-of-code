# Day 11: Chronal Charge

import numpy as np

serial_number = int(open('2018/day11/day11.txt').read())

def power_level(x, y):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    hundreds_digit = (power_level//100)%10
    return hundreds_digit - 5


def get_total_power(top_left_x, top_left_y, size):
    total_power = 0
    for i in range(size):
        for j in range(size):
            x = top_left_x + i
            y = top_left_y + j
            total_power += power_level(x, y)
    return total_power


def find_largest_total_power(size):
    max_power = get_total_power(0, 0, size)
    best_i, best_j = 0, 0
    for i in range(300-size):
        for j in range(300-size):
            total_power = get_total_power(i, j, size)
            if total_power > max_power:
                max_power = total_power
                best_i, best_j = i, j
    return max_power, best_i, best_j


def consider_all_sizes():
    powers = np.fromfunction(power_level, (300, 300))
    best_size, max_power, best_x, best_y = 0, 0, 0, 0
    for size in range(1, 300):
        boxes = sum([powers[x:x-size, y:y-size] for x in range(size) for y in range(size)])
        power = int(boxes.max())
        if power > max_power:
            max_power = power
            best_size = size
            best_x, best_y = np.where(boxes == max_power)
    return best_size, max_power, best_x[0], best_y[0]


def part_1():
    _, best_i, best_j = find_largest_total_power(3)
    return best_i, best_j


def part_2():
    best_size, _, best_x, best_y = consider_all_sizes()
    return best_x, best_y, best_size


print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))
