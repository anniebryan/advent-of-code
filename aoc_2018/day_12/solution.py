"""
Advent of Code 2018
Day 12: Subterranean Sustainability
"""

import click
import os
from pathlib import Path


def get_initial_plant_indices(puzzle_input):
    initial_state = puzzle_input[0].split()[-1]
    indices = {i for i in range(len(initial_state)) if initial_state[i] == '#'}
    return indices


def get_rules(puzzle_input):
    rules = puzzle_input[2:]
    rule_map = {}
    for rule in rules:
        key, _, val = rule.split()
        rule_map[key] = val
    return rule_map


def time_step(indices, rules):
    new_indices = set()
    for i in range(min(indices) - 1, max(indices) + 2):
        s = []
        for j in range(5):
            if i + j - 2 in indices:
                s.append("#")
            else:
                s.append(".")
        if rules.get("".join(s)) == "#":
            new_indices.add(i)
    return new_indices


def run_n_generations(puzzle_input, n):
    indices = get_initial_plant_indices(puzzle_input)
    rules = get_rules(puzzle_input)
    for _ in range(n):
        indices = time_step(indices, rules)
    return indices


def solve_part_1(puzzle_input: list[str]):
    return sum(run_n_generations(puzzle_input, 20))


def solve_part_2(puzzle_input: list[str]):
    return sum(run_n_generations(puzzle_input, 2000)) + (50000000000 - 2000) * 75


@click.command()
@click.option("-se", "--skip_example", is_flag=True, default=False)
@click.option("-sp", "--skip_puzzle", is_flag=True, default=False)
def main(skip_example: bool = False, skip_puzzle: bool = False) -> None:
    base_dir = Path(__file__).parent
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
