"""
Advent of Code 2023
Day 10: Pipe Maze
"""

import os
from collections import defaultdict
from pathlib import Path

import click


class PipeGrid:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.pipes = {}  # maps (i, j) -> character at that location
        self.starting_pos = None
        self.edges = defaultdict(set)  # maps (i, j) -> set of neighbors
        self.main_loop_tiles = None  # set in determine_main_loop

    def in_bounds(self, i: int, j: int) -> bool:
        return 0 <= i <= self.height - 1 and 0 <= j <= self.width - 1

    def add_pipe(self, i: int, j: int, ch: str) -> None:
        if not self.in_bounds(i, j):
            raise ValueError(f"({i}, {j}) not in bounds")

        assert (i, j) not in self.pipes
        self.pipes[(i, j)] = ch

        if ch == ".":
            return

        if ch == "S":
            self.starting_pos = (i, j)
            return

        if ch == "|":
            neighbors = {(i - 1, j), (i + 1, j)}
        elif ch == "-":
            neighbors = {(i, j - 1), (i, j + 1)}
        elif ch == "L":
            neighbors = {(i - 1, j), (i, j + 1)}
        elif ch == "J":
            neighbors = {(i - 1, j), (i, j - 1)}
        elif ch == "7":
            neighbors = {(i, j - 1), (i + 1, j)}
        elif ch == "F":
            neighbors = {(i, j + 1), (i + 1, j)}
        else:
            raise ValueError(f"Unexpected value {ch}")

        for (x, y) in neighbors:
            if self.in_bounds(x, y):
                self.edges[(i, j)].add((x, y))

    def set_starting_pos_neighbors(self) -> None:
        assert self.starting_pos is not None
        starting_pos_neighbors = set()
        for loc, neighbors in self.edges.items():
            if self.starting_pos in neighbors:
                starting_pos_neighbors.add(loc)
        self.edges[self.starting_pos] = starting_pos_neighbors

    def determine_main_loop(self) -> dict[tuple[int, int], int]:
        """Return map from (i, j) -> int distance when traveling along the main loop"""
        dist = 0
        res = {self.starting_pos: 0}
        seen = {self.starting_pos}
        pos_a, pos_b = self.edges[self.starting_pos]
        while (pos_a is not None) and (pos_b is not None):
            dist += 1
            if pos_a is not None and pos_a not in seen:
                res[pos_a] = dist
                seen.add(pos_a)
            if pos_b is not None and pos_b not in seen:
                res[pos_b] = dist
                seen.add(pos_b)

            if len(pos_a_unseen_neighbors := self.edges[pos_a] - seen) == 0:
                pos_a = None
            else:
                pos_a = next(iter(pos_a_unseen_neighbors))

            if len(pos_b_unseen_neighbors := self.edges[pos_b] - seen) == 0:
                pos_b = None
            else:
                pos_b = next(iter(pos_b_unseen_neighbors))
        self.main_loop_tiles = set(res)
        return res

    def determine_start_tile(self) -> str:
        starting_edges = self.edges[self.starting_pos]
        i, j = self.starting_pos
        if starting_edges == {(i - 1, j), (i + 1, j)}:
            return "|"
        if starting_edges == {(i, j - 1), (i, j + 1)}:
            return "-"
        if starting_edges == {(i - 1, j), (i, j + 1)}:
            return "L"
        if starting_edges == {(i - 1, j), (i, j - 1)}:
            return "J"
        if starting_edges == {(i, j - 1), (i + 1, j)}:
            return "7"
        if starting_edges == {(i, j + 1), (i + 1, j)}:
            return "F"
        raise ValueError("Unknown start tile")

    def num_enclosed_tiles(self) -> int:
        _ = self.determine_main_loop()
        VERTICAL = "|LJ"
        num_enclosed = 0
        for i in range(self.height):
            num_vertical_pipes_seen = 0
            for j in range(self.height):
                loc = (i, j)
                ch = self.pipes[loc]
                if loc in self.main_loop_tiles:
                    if ch in VERTICAL or (ch == "S" and self.determine_start_tile() in VERTICAL):
                        num_vertical_pipes_seen += 1
                elif num_vertical_pipes_seen % 2 == 1:
                    num_enclosed += 1
        return num_enclosed


def parse_input(puzzle_input: list[str]) -> PipeGrid:
    pg = PipeGrid(len(puzzle_input), len(puzzle_input[0]))
    for i, line in enumerate(puzzle_input):
        for j, ch in enumerate(line):
            pg.add_pipe(i, j, ch)
    pg.set_starting_pos_neighbors()
    return pg


def solve_part_1(puzzle_input: list[str]):
    pg = parse_input(puzzle_input)
    main_loop = pg.determine_main_loop()
    return max(main_loop.values())


def solve_part_2(puzzle_input: list[str]):
    pg = parse_input(puzzle_input)
    return pg.num_enclosed_tiles()


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
