"""
Advent of Code 2020
Day 19: Monster Messages
"""

import click
import os
import pathlib
import regex as re


def process_input(puzzle_input):
    ix = puzzle_input.index("")
    rules = puzzle_input[:ix]
    messages = puzzle_input[ix + 1:]
    new_rules = {}
    for rule in rules:
        n, d = rule.split(': ')
        new_rules[int(n)] = d
    return new_rules, messages


def build_regex(rules, n, part_2):
    if part_2:
        if n == 8:
            return f'({build_regex(rules, 42, True)}+)'
        if n == 11:
            return f'(?P<{"r0"}>{build_regex(rules, 42, True)}(?P>{"r0"})?{build_regex(rules, 31, True)})'

    rule = rules[n]
    match = re.match(r'"(\w)"', rule)
    if match:
        return match.group(1)
    
    pattern = []
    for sub_rule in rule.split(' | '):
        pattern.append("".join([build_regex(rules, int(m), part_2) for m in sub_rule.split()]))
    return f"({'|'.join(pattern)})"


def num_that_match(rules, messages, part_2):
    num_matches = 0
    for m in messages:
        if re.match(f'^{build_regex(rules, 0, part_2)}$', m):
            num_matches += 1
    return num_matches


def solve_part_1(puzzle_input: list[str]):
    rules, messages = process_input(puzzle_input)
    return num_that_match(rules, messages, False)


def solve_part_2(puzzle_input: list[str]):
    rules, messages = process_input(puzzle_input)
    return num_that_match(rules, messages, True)


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
