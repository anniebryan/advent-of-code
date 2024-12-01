"""
Advent of Code 2020
Day 18: Operation Order
"""

def process_parens(exp, i, add_first):
    num_parens, j = 1, i

    while num_parens != 0:
        j += 1
        if exp[j] == '(':
            num_parens += 1
        if exp[j] == ')':
            num_parens -= 1

    prefix = exp[:i]
    suffix = exp[j + 1:]
    return evaluate_expression(prefix + evaluate_expression(exp[i + 1:j], add_first) + suffix, add_first)


def process_addition(exp, i):
    vals = exp.split()
    first_val, second_val = int(vals[i - 1]), int(vals[i + 1])

    prefix = ' '.join(vals[:i - 1])
    suffix = ' '.join(vals[i + 2:])
    return evaluate_expression(' '.join([prefix, str(first_val + second_val), suffix]), True)


def evaluate_expression(exp, add_first):
    if len(exp.split()) == 1:
        return exp
    if '(' in exp:
        return process_parens(exp, exp.find('('), add_first)
    if add_first and '+' in exp:
        return process_addition(exp, exp.split().index('+'))

    split_vals = exp.split()
    first_val, op, second_val = int(split_vals[0]), split_vals[1], int(split_vals[2])
    rest = ' '.join(split_vals[3:])
    if op == '+':
        return evaluate_expression(' '.join([str(first_val + second_val), rest]), add_first)
    if op == '*':
        return evaluate_expression(' '.join([str(first_val * second_val), rest]), add_first)


def sum_all(puzzle_input, add_first):
    return sum([int(evaluate_expression(line, add_first)) for line in puzzle_input])


def solve_part_1(puzzle_input):
    return sum_all(puzzle_input, False)


def solve_part_2(puzzle_input):
    return sum_all(puzzle_input, True)
