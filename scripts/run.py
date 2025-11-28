#!/usr/bin/env python3
import os
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Callable

import click


def _run_solution(
    base_dir: Path,
    filename: str,
    display_name: str,
    solve_part_1: Callable,
    solve_part_2: Callable,
) -> None:
    print(f"--- {display_name} ---")

    if not (filepath := (base_dir / filename)).exists():
        print(f"{filename} not found.")
        return

    with open(filepath) as file:
        puzzle_input = [line.strip("\n") for line in file]
        print(f"Part 1: {solve_part_1(puzzle_input)}")
        print(f"Part 2: {solve_part_2(puzzle_input)}")


def load_solution_module(year: int, day: int) -> tuple[Callable, Callable]:
    solution_path = Path(f"src/aoc_{year}/day_{day:02d}/solution.py").resolve()
    if not solution_path.exists():
        raise FileNotFoundError(f"{solution_path} does not exist")

    spec = spec_from_file_location("solution", solution_path)
    module = module_from_spec(spec)
    sys.modules["solution"] = module
    spec.loader.exec_module(module)  # type: ignore
    return module.solve_part_1, module.solve_part_2


@click.command()
@click.argument("year", type=int)
@click.argument("day", type=int)
@click.option("-se", "--skip_example", is_flag=True, default=False)
@click.option("-sp", "--skip_puzzle", is_flag=True, default=False)
def main(year: int, day: int, skip_example: bool = False, skip_puzzle: bool = False):

    base_dir = Path(__file__).parent.parent / "src" / f"aoc_{year}" / f"day_{day:02d}"
    example_files = sorted([file for file in os.listdir(base_dir) if file.endswith(".txt") and "example" in file])

    solve_part_1, solve_part_2 = load_solution_module(year, day)

    if not skip_example:
        if len(example_files) < 2:
            _run_solution(base_dir, "example.txt", "Example", solve_part_1, solve_part_2)
        else:
            for i, filename in enumerate(example_files):
                _run_solution(base_dir, filename, f"Example {i + 1}", solve_part_1, solve_part_2)

    if not skip_puzzle:
        _run_solution(base_dir, "puzzle.txt", "Puzzle", solve_part_1, solve_part_2)


if __name__ == "__main__":
    main()
