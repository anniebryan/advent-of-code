"""
Advent of Code 2022
Day 4: Camp Cleanup
"""

def get_sections(puzzle_input):
    for r in puzzle_input:
        elf_one, elf_two = r.split(',')
        a, b = elf_one.split('-')
        c, d = elf_two.split('-')
        yield int(a), int(b), int(c), int(d)


def solve_part_1(puzzle_input):
    num_overlap = 0
    for a, b, c, d in get_sections(puzzle_input):
        if a <= c <= d <= b:
            num_overlap += 1
        elif c <= a <= b <= d:
            num_overlap += 1
    return num_overlap


def solve_part_2(puzzle_input):
    num_overlap = 0
    for a, b, c, d in get_sections(puzzle_input):
        if a <= c <= b:
            num_overlap += 1
        elif c <= a <= d:
            num_overlap += 1
    return num_overlap
