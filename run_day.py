import sys
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

    for input_filename in ["example", "puzzle"]:
        print(f"---{input_filename.capitalize()}---")
        input_filepath = base_dir / f"{input_filename}.txt"
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
