"""
Advent of Code 2021
Day 14: Extended Polymerization
"""

import click
import os
import pathlib
from collections import defaultdict, deque


def get_template(puzzle_input):
    template = puzzle_input[0].strip()
    return template


def get_rules(puzzle_input):
    rules = [tuple(rule.strip().split(' -> ')) for rule in puzzle_input[2:]]
    return rules


def execute_rules(rules, text):
    new_text = deque()
    for rule in rules:
        pair, char = rule
        a_valid = False
        while text:
            while not a_valid:
                (a, a_valid) = text.popleft()
                new_text.append((a, a_valid))

            (b, b_valid) = text.popleft()
            while not b_valid:
                new_text.append((b, b_valid))
                (b, b_valid) = text.popleft()
            if f'{a}{b}' == pair:
                new_text.append((char, False))
            new_text.append((b, b_valid))
            (a, a_valid) = (b, b_valid)
        while new_text:
            text.append(new_text.popleft())
    return text

def n_steps(rules, text, n):
    for _ in range(n):
        new_text = execute_rules(rules, text)
        text = deque()
        while new_text:
            char, _ = new_text.popleft()
            text.append((char, True))
    return text


def difference(text):
    counts = defaultdict(int)
    for s in text:
        counts[s] += 1
    
    most_common = max(counts, key=counts.get)
    least_common = min(counts, key=counts.get)

    return counts[most_common] - counts[least_common]


def solve_part_1(puzzle_input: list[str]):
    template = get_template(puzzle_input)
    rules = get_rules(puzzle_input)
    text = deque()
    for s in template:
        text.append((s, True))
    text = n_steps(rules, text, 10)
    return difference(text)


# TODO speedup
def solve_part_2(puzzle_input: list[str]):
    template = get_template(puzzle_input)
    rules = get_rules(puzzle_input)
    text = deque()
    for s in template:
        text.append((s, True))
    text = n_steps(rules, text, 40)
    return difference(text)


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
