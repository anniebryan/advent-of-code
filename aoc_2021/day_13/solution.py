"""
Advent of Code 2021
Day 13: Transparent Origami
"""

def get_dots_instructions(puzzle_input):
    dots, instructions = [], []
    is_instruction = False
    for line in puzzle_input:
        if line == "":
            is_instruction = True
        elif is_instruction:
            instructions.append(tuple([line.split('=')[0][-1], int(line.split('=')[1])]))
        else:
            dots.append(tuple([int(val) for val in line.split(',')]))
    return dots, instructions


def fold(dots, dir, val):
    new_dots = set()
    for dot in dots:
        x, y = dot
        if dir == 'x':
            new_x = x if val > x else 2 * val - x
            new_dot = (new_x, y)
        else:
            new_y = y if val > y else 2 * val - y
            new_dot = (x, new_y)
        new_dots.add(new_dot)
    return new_dots


def visualize(dots):
    max_x = max([dot[0] for dot in dots])
    max_y = max([dot[1] for dot in dots])

    s = ["\n"]
    for j in range(max_y + 1):
        row = ["#" if (i, j) in dots else "." for i in range(max_x + 1)]
        s.append("".join(row))
    return "\n".join(s)


def solve_part_1(puzzle_input):
    dots, instructions = get_dots_instructions(puzzle_input)
    dir, val = instructions[0]
    return len(fold(dots, dir, val))


def solve_part_2(puzzle_input):
    dots, instructions = get_dots_instructions(puzzle_input)
    for instruction in instructions:
        dir, val = instruction
        dots = fold(dots, dir, val)
    return visualize(dots)
