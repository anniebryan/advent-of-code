#!/usr/bin/env python3
import sys
import requests
from pathlib import Path
from string import Template

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent

TEMPLATE_FILE = SCRIPTS_DIR / "template.py"
CONFIG_FILE = SCRIPTS_DIR / "config.txt"


def download_puzzle_input(year: int, day: int, dest_file: Path) -> None:
    if not CONFIG_FILE.exists():
        print("config.txt not found — skipping puzzle download.")
        return

    session = CONFIG_FILE.read_text().strip()
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(url, cookies={"session": session})

    if response.status_code != 200:
        print(f"Failed to download puzzle input (HTTP {response.status_code})")
        return

    dest_file.write_text(response.text.rstrip("\n"))
    print(f"Downloaded puzzle → {dest_file}")


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python scripts/create_day.py <year> <day>")
        sys.exit(1)

    year = int(sys.argv[1])
    day = int(sys.argv[2])

    target_dir = REPO_ROOT / f"aoc_{year}" / f"day_{day:02d}"
    target_dir.mkdir(parents=True, exist_ok=True)

    solution_file = target_dir / "solution.py"
    example_file = target_dir / "example.txt"
    puzzle_file = target_dir / "puzzle.txt"

    if solution_file.exists():
        print(f"{solution_file} already exists — not overwriting.")
    else:
        template = Template(TEMPLATE_FILE.read_text())
        print(template)
        template = template.substitute(YEAR=year, DAY=day)
        solution_file.write_text(template)
        print(f"Created {solution_file}")

    if example_file.exists():
        print(f"{example_file} already exists — not overwriting.")
    else:
        example_file.write_text("")
        print(f"Created {example_file}")

    if puzzle_file.exists() and puzzle_file.read_text():
        print(f"{puzzle_file} already exists and is non-empty — skipping download.")
    else:
        session = CONFIG_FILE.read_text().strip()
        url = f"https://adventofcode.com/{year}/day/{day}/input"
        response = requests.get(url, cookies={"session": session})
        if response.status_code != 200:
            print(f"Failed to download puzzle input (HTTP {response.status_code})")
        else:
            print(f"Successfully downloaded puzzle input (HTTP {response.status_code})")
            puzzle_input = response.text.strip("\n")
            puzzle_file.write_text(puzzle_input)
            print(f"Created {puzzle_file}")

    print("Done!")


if __name__ == "__main__":
    main()
