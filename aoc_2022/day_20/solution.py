"""
Advent of Code 2022
Day 20: Grove Positioning System
"""

import click
import os
import pathlib


# TODO move to utils
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

    def link(self, node: "Node") -> None:
        self.next = node
        node.prev = self


# TODO move to utils
class LinkedList:
    def __init__(self, decryption_key):
        self.nodes = []
        self.length = 0
        self.first_node = None
        self.last_node = None
        self.zero_node = None
        self.decryption_key = decryption_key

    def add_node(self, val):
        node = Node(val * self.decryption_key)

        if self.first_node is None:
            self.first_node = node
            self.last_node = node

        if val == 0:
            self.zero_node = node

        node.link(self.first_node)
        self.last_node.link(node)

        self.last_node = node
        self.nodes.append(node)
        self.length += 1

    def move_node(self, node):
        num_spaces = node.val % (self.length - 1)
        if num_spaces != 0:
            p = node
            for _ in range(num_spaces):
                p = p.next
            node.prev.link(node.next)
            n = p.next
            p.link(node)
            node.link(n)

    def num_after_zero(self, num):
        i = num % self.length
        node = self.zero_node
        for _ in range(i):
            node = node.next
        return node.val


def parse(puzzle_input, decryption_key):
    ls = LinkedList(decryption_key)
    for row in puzzle_input:
        ls.add_node(int(row))
    return ls


def solve(puzzle_input, decryption_key, num_times):
    ls = parse(puzzle_input, decryption_key)
    nodes = ls.nodes
    for _ in range(num_times):
        for node in nodes:
            ls.move_node(node)
    return sum([ls.num_after_zero(i) for i in [1000, 2000, 3000]])


def solve_part_1(puzzle_input: list[str]):
    return solve(puzzle_input, 1, 1)


def solve_part_2(puzzle_input: list[str]):
    return solve(puzzle_input, 811589153, 10)


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
