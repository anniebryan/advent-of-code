#!/usr/bin/env python3
import re
import sys
import traceback
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Callable

import click


def _read_puzzle_input(base_dir: Path, filename: str) -> list[str] | None:

    filepath = base_dir / filename
    if not filepath.exists():
        print(f"{filename} not found.")
        return None

    try:
        puzzle_input = filepath.read_text().splitlines()
        return puzzle_input
    except Exception as exc:
        print(f"Failed to read {filepath}: {exc}")
        return None


def _run_test_case(num: int, puzzle_input: list[str], solve_fn: Callable) -> None:
    try:
        print(f"Part {num}: {solve_fn(puzzle_input)}")
    except Exception:
        print(f"Part {num}: ERROR")
        traceback.print_exc()


def load_solution_module(year: int, day: int) -> tuple[Callable, Callable]:
    solution_path = Path(f"src/aoc_{year}/day_{day:02d}/solution.py").resolve()
    if not solution_path.exists():
        raise FileNotFoundError(f"{solution_path} does not exist")

    module_name = f"aoc_{year}_day_{day:02d}_solution"
    spec = spec_from_file_location(module_name, solution_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Couldn't create import spec for {solution_path}")
    module = module_from_spec(spec)  # type: ignore

    try:
        sys.modules[module_name] = module
        spec.loader.exec_module(module)  # type: ignore
    except Exception as exc:
        # cleanup any partially-registered module to avoid confusing subsequent imports
        sys.modules.pop(module_name, None)
        raise RuntimeError(f"Failed to import {solution_path}: {exc}")

    if not hasattr(module, "solve_part_1") or not hasattr(module, "solve_part_2"):
        raise AttributeError(f"{module_name} missing solve_part_1/solve_part_2")

    if not callable(module.solve_part_1) or not callable(module.solve_part_2):
        raise TypeError("solve_part_1 and solve_part_2 must be callable")

    return module.solve_part_1, module.solve_part_2


def _run_day(
        year: int,
        day: int,
        skip_example: bool = False,
        skip_puzzle: bool = False,
        part1_only: bool = False,
        part2_only: bool = False,
) -> None:
    """Runs the solution for a single day."""
    base_dir = Path(__file__).parent.parent / "src" / f"aoc_{year}" / f"day_{day:02d}"
    if not base_dir.exists():
        print(f"Day directory {base_dir} does not exist")
        return
    
    input_dir = base_dir / "input"
    if not input_dir.exists():
        print(f"Input directory {input_dir} does not exist")
        return

    print(f"\n=== Day {day:02d} ===\n")

    try:
        solve_part_1, solve_part_2 = load_solution_module(year, day)
    except Exception as exc:
        print(f"Skipping day {day:02d}: {exc}")
        return

    if not skip_example:
        example_files = sorted([p.name for p in input_dir.glob("*example*.txt")])
        if not example_files:
            print("No example files found.")
        for example_file in example_files:
            print(f"--- Example ({example_file}) ---")
            puzzle_input = _read_puzzle_input(input_dir, example_file)
            if puzzle_input is not None:
                if not part2_only:
                    _run_test_case(1, puzzle_input, solve_part_1)
                if not part1_only:
                    _run_test_case(2, puzzle_input, solve_part_2) 

    if not skip_puzzle:
        puzzle_file = "puzzle.txt"
        print(f"--- Puzzle ({puzzle_file}) ---")
        puzzle_input = _read_puzzle_input(input_dir, puzzle_file)
        if puzzle_input is not None:
            if not part2_only:
                _run_test_case(1, puzzle_input, solve_part_1)
            if not part1_only:
                _run_test_case(2, puzzle_input, solve_part_2)


def _run_year(
        year: int,
        skip_example: bool = False,
        skip_puzzle: bool = False,
        part1_only: bool = False,
        part2_only: bool = False,
) -> None:
    year_dir = Path(__file__).parent.parent / "src" / f"aoc_{year}"
    if not year_dir.exists():
        print(f"Year directory {year_dir} does not exist")
        return

    day_dirs = sorted([d for d in year_dir.iterdir() if d.is_dir() and re.match(r"day_\d{2}$", d.name)])
    if not day_dirs:
        print(f"No directories were found matching {year_dir}/day_DD/")
        return

    for day_dir in day_dirs:
        m = re.match(r"day_(\d{2})$", day_dir.name)
        if not m:
            continue
        day = int(m.group(1))
        _run_day(year, day, skip_example, skip_puzzle, part1_only, part2_only)


def _run_all(
        skip_example: bool = False,
        skip_puzzle: bool = False,
        part1_only: bool = False,
        part2_only: bool = False,
) -> None:
    root_dir = Path(__file__).parent.parent / "src"

    year_dirs = sorted([d for d in root_dir.iterdir() if d.is_dir() and re.match(r"aoc_\d{4}$", d.name)])
    if not year_dirs:
        print("No directories were found matching aoc_YYYY/")
        return

    for year_dir in year_dirs:
        m = re.match(r"aoc_(\d{4})$", year_dir.name)
        if not m:
            continue
        year = int(m.group(1))
        _run_year(year, skip_example, skip_puzzle, part1_only, part2_only)


@click.group()
def cli() -> None:
    """CLI group for running solutions."""
    pass


def _validate_flags(skip_example: bool, skip_puzzle: bool, part1_only: bool, part2_only: bool) -> None:
    if skip_example and skip_puzzle:
        print("Error: --skip-example and --skip-puzzle cannot both be set.")
        raise SystemExit(2)
    if part1_only and part2_only:
        print("Error: --part1-only and --part2-only are mutually exclusive.")
        raise SystemExit(2)
    

COMMON_OPTIONS = [
    click.option("-se", "--skip-example", "skip_example", is_flag=True, default=False),
    click.option("-sp", "--skip-puzzle", "skip_puzzle", is_flag=True, default=False),
    click.option("-p1", "--part1-only", "part1_only", is_flag=True, default=False),
    click.option("-p2", "--part2-only", "part2_only", is_flag=True, default=False),
]


def apply_options(options):
    def decorator(f):
        for option in reversed(options):
            f = option(f)
        return f
    return decorator


@cli.command(name="run")
@click.argument("year", type=int)
@click.argument("day", type=int)
@apply_options(COMMON_OPTIONS)
def run_cmd(year: int, day: int, skip_example: bool, skip_puzzle: bool, part1_only: bool, part2_only: bool) -> None:
    _validate_flags(skip_example, skip_puzzle, part1_only, part2_only)
    _run_day(year, day, skip_example, skip_puzzle, part1_only, part2_only)


@cli.command(name="run-year")
@click.argument("year", type=int)
@apply_options(COMMON_OPTIONS)
def run_year_cmd(year: int, skip_example: bool, skip_puzzle: bool, part1_only: bool, part2_only: bool) -> None:
    _validate_flags(skip_example, skip_puzzle, part1_only, part2_only)
    _run_year(year, skip_example, skip_puzzle, part1_only, part2_only)


@cli.command(name="run-all")
@apply_options(COMMON_OPTIONS)
def run_all_cmd(skip_example: bool, skip_puzzle: bool, part1_only: bool, part2_only: bool) -> None:
    _validate_flags(skip_example, skip_puzzle, part1_only, part2_only)
    _run_all(skip_example, skip_puzzle, part1_only, part2_only)


if __name__ == "__main__":
    cli()
