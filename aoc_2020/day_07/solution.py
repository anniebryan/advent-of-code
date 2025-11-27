"""
Advent of Code 2020
Day 7: Handy Haversacks
"""

import os
from collections import defaultdict, deque
from pathlib import Path

import click
import regex as re

SHINY_GOLD = 'shiny gold'


def get_containers(puzzle_input):
    """
    returns a dictionary that maps a string to a set of strings
    with all bags that can contain that string
    """
    containers = defaultdict(set)
    for rule in puzzle_input:
        outer_bag = re.match('([A-Za-z ]+) bags', rule)[1]
        inner_bags = re.findall(r'(\d+) ([A-Za-z ]+?) bags?', rule)
        for bag in inner_bags:
            containers[bag[1]].add(outer_bag)
    return containers


def get_num_containing(puzzle_input):
    """
    returns a dictionary that maps a string to a set of tuples (n, b)
    such that the key must contain n bags of type b
    """
    containing = {}
    for rule in puzzle_input:
        outer_bag = re.match(r'([A-Za-z ]+) bags', rule)[1].split(" bags contain no other")[0]
        inner_bags = re.findall(r'(\d+) ([A-Za-z ]+?) bags?', rule)
        containing[outer_bag] = {(int(t[0]), t[1]) for t in inner_bags}
    return containing


def get_all_possible_containers(puzzle_input, color):
    containers = get_containers(puzzle_input)
    possible = set()
    seen = set()
    queue = deque()
    queue.append(color)
    while queue:
        c = queue.pop()
        for container in containers[c]:
            if container not in seen:  # prevents cycles
                possible.add(container)
                seen.add(container)
                queue.append(container)
    return possible


def get_total_num_containing(color, containing):
    num_containing = 0
    for t in containing[color]:
        num_containing += t[0] * (1 + get_total_num_containing(t[1], containing))
    return num_containing


def solve_part_1(puzzle_input: list[str]):
    return len(get_all_possible_containers(puzzle_input, SHINY_GOLD))


def solve_part_2(puzzle_input: list[str]):
    return get_total_num_containing(SHINY_GOLD, get_num_containing(puzzle_input))


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
