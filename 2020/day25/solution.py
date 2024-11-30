from collections import defaultdict

def get_public_keys(puzzle_input):
    return [int(key) for key in puzzle_input]

def get_loop_size(keys, subject_number, upper_bound):
    for i, val in transform(subject_number, upper_bound):
        if val in keys:
            return i, val

def transform(subject_number, loop_size):
    val = 1
    for i in range(loop_size):
        val *= subject_number
        val %= 20201227
        yield i+1, val

def other_key(keys, key):
    if key == keys[0]: return keys[1]
    else: return keys[0]

def part_1(puzzle_input):
    keys = get_public_keys(puzzle_input)
    loop_size, key = get_loop_size(keys, 7, 10000000)
    return list(transform(other_key(keys, key), loop_size))[-1][1]

def part_2(puzzle_input):
    return
