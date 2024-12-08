"""
Advent of Code 2024
Day 5: Print Queue
"""

import click
import os
import pathlib
from collections import defaultdict, deque


class DirectedGraph:
    def __init__(self):
        self.graph = defaultdict(set)

    def insert_edge(self, x: int, y: int):
        self.graph[x].add(y)

    def path_exists(self, nums: list[int]) -> bool:
        for n1, n2 in zip(nums, nums[1:]):
            if n2 not in self.graph[n1]:
                return False
        return True
    
    def reorder(self, line: list[str]) -> list[str]:
        q = deque()
        for val in line:
            q.append(([val], val, set(line) - {val}))
        while q:
            path, last, remaining = q.popleft()
            if len(remaining) == 0:
                return path
            for r in remaining:
                if r in self.graph[last]:
                    q.append((path + [r], r, remaining - {r}))
        raise ValueError("Could not find a valid order")


def parse_input(puzzle_input: list[str]) -> tuple[DirectedGraph, list[list[int]]]:
    g = DirectedGraph()
    updates = []
    end_of_rules = None
    for i, line in enumerate(puzzle_input):
        if line == "":
            end_of_rules = i
        elif end_of_rules is None:
            [x, y] = [int(d) for d in line.split("|")]
            g.insert_edge(x, y)
        else:
            updates.append([int(d) for d in line.split(",")])
    return g, updates


def middle_number(line: list[int]) -> int:
    return line[len(line) // 2]


def solve_part_1(puzzle_input: list[str]):
    g, updates = parse_input(puzzle_input)

    middle_nums = []
    for line in updates:
        if g.path_exists(line):
            middle_nums.append(middle_number(line))

    return sum(middle_nums)


# TODO speedup
def solve_part_2(puzzle_input: list[str]):
    g, updates = parse_input(puzzle_input)

    middle_nums = []
    for line in updates:
        if not g.path_exists(line):
            ordered_line = g.reorder(line)
            assert g.path_exists(ordered_line)
            middle_nums.append(middle_number(ordered_line))

    return sum(middle_nums)


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
