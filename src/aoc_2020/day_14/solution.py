"""
Advent of Code 2020
Day 14: Docking Data
"""

def binary(n):
    return str(bin(int(n)))[2:]


def base_10(n):
    return int(n, 2)


def get_mask(line):
    return {i: char for i, char in enumerate(line.split()[2][::-1])}


def get_memory_values(line, mask, part_one):
    a, v = line.split()[0][4:-1], line.split()[2]
    if part_one:
        address = int(a)
        value = base_10(apply_mask(binary(v), mask, True))
    else:
        address = get_all_addresses(apply_mask(binary(a), mask, False))
        value = int(v)
    return (address, value)


def apply_mask(s, mask, part_one):
    new_s = ''
    for i in range(max(mask) + 1):
        if part_one:
            if mask[i] in {'0', '1'}:
                new_s += mask[i]
            else:
                new_s += ('0' if i >= len(s) else s[len(s) - 1 - i])
        else:
            if mask[i] == '0':
                new_s += ('0' if i >= len(s) else s[len(s) - 1 - i])
            else:
                new_s +=  mask[i]
    return new_s[::-1]


def get_all_addresses(s):
    addresses = {s}
    x_indices = [i for i, c in enumerate(s) if c == 'X']
    for i in x_indices:
        new_addresses = set()
        for a in addresses:
            for c in {'0', '1'}:
                new_addresses.add(a[:i] + c + a[i + 1:])
        addresses = new_addresses
    return {base_10(a) for a in addresses}


def process_program(puzzle_input, part_one):
    memory = {}
    mask = {}
    for line in puzzle_input:
        if line[:4] == 'mask':
            mask = get_mask(line)
        else:
            key, val = get_memory_values(line, mask, part_one)
            if part_one:
                memory[key] = val
            else:
                for k in key:
                    memory[k] = val
    return memory


def solve_part_1(puzzle_input: list[str]):
    return sum(process_program(puzzle_input, True).values())


def solve_part_2(puzzle_input: list[str]):
    return sum(process_program(puzzle_input, False).values())
