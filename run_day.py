import sys
import os
import importlib.util
from pathlib import Path


def main(year: str, day: str) -> None:
    base_dir = Path(f"{year}/day{day}")
    file_path = base_dir / "solution.py"

    if file_path.exists():
        spec = importlib.util.spec_from_file_location(f"day{day}", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        raise FileNotFoundError(f"File {file_path} does not exist. Run `sh create_day.sh {year} {day}` to create it.")

    part_1 = getattr(module, "part_1", None)
    part_2 = getattr(module, "part_2", None)

    input_files = [fname for fname in os.listdir(base_dir) if fname.endswith(".txt")]
    ex_input_files = sorted([fname for fname in input_files if fname != "puzzle.txt"])
    if len(ex_input_files) == 0:
        ex_input_files, ex_display_names = ["example.txt"], ["Example"]
    elif len(ex_input_files) == 1:
        ex_display_names = ["Example"]
    else:
        ex_display_names = [f"Example {i + 1}" for i in range(len(ex_input_files))]

    for input_filename, display_name in zip(ex_input_files + ["puzzle.txt"], ex_display_names + ["Puzzle"]):
        print(f"---{display_name}---")
        input_filepath = base_dir / input_filename
        if not input_filepath.exists():
            print("Input file not found.")
            continue
        with open(input_filepath) as file:
            puzzle_input = [line.strip("\n") for line in file]
            print(f"Part 1: {part_1(puzzle_input)}")
            print(f"Part 2: {part_2(puzzle_input)}")


if __name__ == "__main__":
    year, day = sys.argv[1:]
    main(year, day)
