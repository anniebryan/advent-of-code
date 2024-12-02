"""
Advent of Code 2022
Day 21: Monkey Math
"""

import click
import os
import pathlib
import re
import operator

OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
}

INVERSE_OPS = {
    "+": operator.sub,
    "-": operator.add,
    "*": operator.truediv,
    "/": operator.mul
}


# TODO move to utils
class Expression:
    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.op_symbol = operation

    def __str__(self):
        return f"({self.left} {self.op_symbol} {self.right})"


class Monkey:
    def __init__(self, row):
        match = re.match(f"(.*): (\d+)", row)
        if match is not None:
            (name, number) = match.groups()
            self.name = name
            self.number = int(number)
        else:
            match = re.match(f"(.*): (.*) (\+|\-|\*|\/) (.*)", row)
            assert(match is not None)
            (name, monkey_one, operation, monkey_two) = match.groups()
            self.name = name
            self.number = None
            self.monkey_one_name = monkey_one
            self.monkey_two_name = monkey_two
            self.operation = operation

    def get_number(self, monkeys):
        if self.number is not None:
            return self.number

        left_val = monkeys[self.monkey_one_name].get_number(monkeys)
        right_val = monkeys[self.monkey_two_name].get_number(monkeys)

        if isinstance(left_val, int) and isinstance(right_val, int):
            return int(OPS[self.operation](left_val, right_val))
        else:
            return Expression(left_val, right_val, self.operation)


def parse(puzzle_input):
    monkeys = {}
    for row in puzzle_input:
        monkey = Monkey(row)
        monkeys[monkey.name] = monkey
    return monkeys


def set_equal(monkeys):
    root_monkey = monkeys["root"]
    monkeys["humn"].number = "X"
    target_value = monkeys[root_monkey.monkey_two_name].get_number(monkeys)
    expression = monkeys[root_monkey.monkey_one_name].get_number(monkeys)
    while not ((isinstance(expression, str)) or isinstance(expression.left, int) and isinstance(expression.right, int)):
        if isinstance(expression.right, int):
            target_value = int(INVERSE_OPS[expression.op_symbol](target_value, expression.right))
            expression = expression.left
        elif isinstance(expression.left, int):
            if expression.op_symbol in {"+", "*"}:
                target_value = int(INVERSE_OPS[expression.op_symbol](target_value, expression.left))
            else:
                target_value = int(OPS[expression.op_symbol](expression.left, target_value))
            expression = expression.right
    return target_value


def solve_part_1(puzzle_input: list[str]):
    monkeys = parse(puzzle_input)
    return monkeys["root"].get_number(monkeys)

    
def solve_part_2(puzzle_input: list[str]):
    monkeys = parse(puzzle_input)
    return set_equal(monkeys)


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
