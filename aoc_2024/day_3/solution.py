"""
Advent of Code 2024
Day 3
"""

import click
import os
import pathlib
import regex as re

PATTERN = r'mul\((?P<n1>\d+),(?P<n2>\d+)\)'


def get_enabled_indices(mem: str) -> set[int]:
    enabled_indices = set()
    is_enabled = True
    for i in range(len(mem)):
        if mem[i:].startswith("do()"):
            is_enabled = True
        elif mem[i:].startswith("don't()"):
            is_enabled = False
        
        if is_enabled:
            enabled_indices.add(i)
    return enabled_indices


def solve_part_1(puzzle_input: list[str]):
    mem = "".join(puzzle_input)

    results = []
    nums = re.findall(PATTERN, mem)
    for (n1, n2) in nums:
        res = int(n1) * int(n2)
        results.append(res)
    return sum(results)


def solve_part_2(puzzle_input: list[str]):
    mem = "".join(puzzle_input)
    enabled_indices = get_enabled_indices(mem)

    results = []
    nums = re.finditer(PATTERN, mem)
    for num in nums:
        ix = num.start(0)
        n1, n2 = num.group("n1"), num.group("n2")
        if ix in enabled_indices:
            res = int(n1) * int(n2)
            results.append(res)
    return sum(results)


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
