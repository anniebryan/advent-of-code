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


def run_day(year: int, day: int, skip_example: bool = False, skip_puzzle: bool = False) -> None:
    """Runs the solution for a single day."""
    base_dir = Path(__file__).parent.parent / "src" / f"aoc_{year}" / f"day_{day:02d}"
    if not base_dir.exists():
        print(f"Day directory {base_dir} does not exist")
        return

    print(f"=== Day {day:02d} ===")

    example_files = sorted([file for file in os.listdir(base_dir) if file.endswith(".txt") and "example" in file])

    solve_part_1, solve_part_2 = load_solution_module(year, day)

    if not skip_example:
        for example_file in example_files:
            _run_solution(
                base_dir,
                example_file,
                f"Example ({example_file})",
                solve_part_1,
                solve_part_2,
            )

    if not skip_puzzle:
        _run_solution(
            base_dir,
            "input.txt",
            "Puzzle Input",
            solve_part_1,
            solve_part_2,
        )

@click.group()
def cli() -> None:
    """CLI group for running solutions."""
    pass


@cli.command(name="run")
@click.argument("year", type=int)
@click.argument("day", type=int)
@click.option("-se", "--skip_example", is_flag=True, default=False)
@click.option("-sp", "--skip_puzzle", is_flag=True, default=False)
def run_cmd(year: int, day: int, skip_example: bool = False, skip_puzzle: bool = False) -> None:
    """Runs the solution for a single day."""
    run_day(year, day, skip_example, skip_puzzle)


@cli.command(name="run-all")
@click.argument("year", type=int)
def run_all(year: int) -> None:
    """Runs all available days for a given year."""

    year_dir = Path(__file__).parent.parent / "src" / f"aoc_{year}"
    if not year_dir.exists():
        print(f"Year directory {year_dir} does not exist")
        return

    day_dirs = sorted([d for d in year_dir.iterdir() if d.is_dir() and d.name.startswith("day_")])
    if not day_dirs:
        print(f"No directories found in {year_dir}")
        return

    for day_dir in day_dirs:
        run_day(year, int(day_dir.name.split("_")[1]), False, False)


if __name__ == "__main__":
    cli()
