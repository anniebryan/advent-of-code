import click
import os
import importlib.util
from pathlib import Path
from typing import Callable


def run_solution(base_dir: Path, input_filename: str, display_name: str, part_1: Callable, part_2: Callable) -> None:
    print(f"--- {display_name} ---")
    input_filepath = base_dir / input_filename
    if not input_filepath.exists():
        print(f"Input file {input_filename} not found.")
        return
    with open(input_filepath) as file:
        puzzle_input = [line.strip("\n") for line in file]
        print(f"Part 1: {part_1(puzzle_input)}")
        print(f"Part 2: {part_2(puzzle_input)}")
    return


@click.command()
@click.argument("year")
@click.argument("day")
@click.option("-se", "--skip_example", is_flag=True, default=False)
@click.option("-sp", "--skip_puzzle", is_flag=True, default=False)
def main(year: str, day: str, skip_example: bool = False, skip_puzzle: bool = False) -> None:
    base_dir = Path(f"aoc_{year}/day_{day}")
    
    if not (file_path := base_dir / "solution.py").exists():
        raise FileNotFoundError(f"File {file_path} does not exist. Run `sh create_day.sh {year} {day}` to create it.")

    spec = importlib.util.spec_from_file_location(f"day_{day}", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    part_1 = getattr(module, "solve_part_1", None)
    part_2 = getattr(module, "solve_part_2", None)

    input_files = [fname for fname in os.listdir(base_dir) if fname.endswith(".txt")]
    example_files = sorted([fname for fname in input_files if fname != "puzzle.txt"])
    if len(example_files) == 0:
        example_files, ex_display_names = ["example.txt"], ["Example"]
    elif len(example_files) == 1:
        ex_display_names = ["Example"]
    else:
        ex_display_names = [f"Example {i + 1}" for i in range(len(example_files))]

    if not skip_example:
        for input_filename, display_name in zip(example_files, ex_display_names):
            run_solution(base_dir, input_filename, display_name, part_1, part_2)
    
    if not skip_puzzle:
        run_solution(base_dir, "puzzle.txt", "Puzzle", part_1, part_2)


if __name__ == "__main__":
    main()
