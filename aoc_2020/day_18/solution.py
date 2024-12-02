"""
Advent of Code 2020
Day 18: Operation Order
"""

import click
import os
import pathlib


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


def solve_part_1(puzzle_input: list[str]):
    return sum_all(puzzle_input, False)


def solve_part_2(puzzle_input: list[str]):
    return sum_all(puzzle_input, True)


@click.command()
@click.option("-se", "--skip_example", is_flag=True, default=False)
@click.option("-sp", "--skip_puzzle", is_flag=True, default=False)
def main(skip_example: bool = False, skip_puzzle: bool = False) -> None:
    base_dir = pathlib.Path(__file__).parent
    example_files = sorted([fn for fn in os.listdir(base_dir) if fn.endswith(".txt") and "example" in fn])

    def _run_solution(filename: str, display_name: str):
        print(f"--- {display_name} ---")

        if not (filepath := (base_dir / filename)).exists():
            print(f"{filename} not found.")
            return

        with open(filepath) as file:
            puzzle_input = [line.strip("\n") for line in file]
            print(f"Part 1: {solve_part_1(puzzle_input)}")
            print(f"Part 2: {solve_part_2(puzzle_input)}")
        return

    if not skip_example:
        if len(example_files) < 2:
            _run_solution("example.txt", "Example")
        else:
            for i, filename in enumerate(example_files):
                _run_solution(filename, f"Example {i + 1}")

    if not skip_puzzle:
        _run_solution("puzzle.txt", "Puzzle")


if __name__ == "__main__":
    main()
