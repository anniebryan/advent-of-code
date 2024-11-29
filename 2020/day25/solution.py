from collections import defaultdict

filename = '2020/day25/day25.txt'
puzzle_input = open(filename).readlines()

def get_public_keys():
    return [int(key) for key in puzzle_input]

def get_loop_size(subject_number, upper_bound):
    keys = get_public_keys()
    for i, val in transform(subject_number, upper_bound):
        if val in keys:
            return i, val

def transform(subject_number, loop_size):
    val = 1
    for i in range(loop_size):
        val *= subject_number
        val %= 20201227
        yield i+1, val

def other_key(key):
    keys = get_public_keys()
    if key == keys[0]: return keys[1]
    else: return keys[0]

def part_1():
    loop_size, key = get_loop_size(7, 10000000)
    return list(transform(other_key(key), loop_size))[-1][1]

print("Part 1: {}".format(part_1()))