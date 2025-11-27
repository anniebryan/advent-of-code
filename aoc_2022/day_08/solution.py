"""
Advent of Code 2022
Day 8: Treetop Tree House
"""

import os
from pathlib import Path

import click


class Forest:
    def __init__(self, grid):
        self.height = len(grid)
        self.width = len(grid[0])
        self.trees = {}
        for i in range(self.height):
            self.trees[i] = {}
            for j in range(self.width):
                self.trees[i][j] = int(grid[i][j])

    def trees_to_edge(self, i, j):
        top = [self.trees[x][j] for x in range(i)][::-1]
        bottom = [self.trees[x][j] for x in range(i + 1, self.height)]
        left = [self.trees[i][y] for y in range(j)][::-1]
        right = [self.trees[i][y] for y in range(j + 1, self.width)]
        return (top, bottom, left, right)

    def is_visible(self, i, j):
        tree_height = self.trees[i][j]
        for dir in self.trees_to_edge(i, j):
            if len(dir) == 0 or tree_height > max(dir):
                return True
        return False

    def scenic_score(self, i, j):
        score = 1
        for dir in self.trees_to_edge(i, j):
            num_visible = 0
            for tree in dir:
                num_visible += 1
                if tree >= self.trees[i][j]:
                    break
            score *= num_visible
        return score


def solve_part_1(puzzle_input: list[str]):
    forest = Forest(puzzle_input)
    visible_trees = 0
    for i in range(forest.height):
        for j in range(forest.width):
            if forest.is_visible(i, j):
                visible_trees += 1
    return visible_trees


def solve_part_2(puzzle_input: list[str]):
    forest = Forest(puzzle_input)
    max_scenic_score = 0
    for i in range(forest.height):
        for j in range(forest.width):
            max_scenic_score = max(max_scenic_score, forest.scenic_score(i, j))
    return max_scenic_score


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
