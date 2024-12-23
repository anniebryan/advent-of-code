"""
Advent of Code 2024
Day 20: Race Condition
"""

import click
import os
import pathlib
from utils import Grid


def get_cheat_candidates(g: Grid) -> set[tuple[tuple[int, int], tuple[int, int]]]:
    cands = set()
    for (s_i, s_j) in g.where(".") + g.where("S"):
        for (n_i, n_j) in [(s_i + 1, s_j), (s_i - 1, s_j), (s_i, s_j + 1), (s_i, s_j - 1)]:
            if g.in_bounds(n_i, n_j) and g.at(n_i, n_j) == "#":
                for (m_i, m_j) in [(n_i + 1, n_j), (n_i - 1, n_j), (n_i, n_j + 1), (n_i, n_j - 1)]:
                    if (m_i, m_j) != (s_i, s_j) and g.in_bounds(m_i, m_j) and g.at(m_i, m_j) in ".E":
                        cands.add(((s_i, s_j), (m_i, m_j)))
    return cands


def solve_part_1(puzzle_input: list[str]):
    g = Grid(puzzle_input)

    start = g.where("S")[0]
    end = g.where("E")[0]
    dists_from_start = g.dijkstra(start)
    dists_from_end = g.dijkstra(end)
    len_without_cheating = dists_from_start[end]

    tot = 0
    cheat_candidates = get_cheat_candidates(g)
    for (c_s, c_e) in cheat_candidates:
        if dists_from_start[c_s] < dists_from_start[c_e]:
            dist_with_cheat = dists_from_start[c_s] + 2 + dists_from_end[c_e]
            if len_without_cheating - dist_with_cheat >= 100:
                tot += 1
    return tot


# TODO
def solve_part_2(puzzle_input: list[str]):
    return


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
