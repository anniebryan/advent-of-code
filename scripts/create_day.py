#!/usr/bin/env python3
import re
import subprocess
import sys
from pathlib import Path
from string import Template

import requests
from bs4 import BeautifulSoup

SCRIPTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPTS_DIR.parent / "src"

TEMPLATE_FILE = SCRIPTS_DIR / "template.py.tpl"
CONFIG_FILE = SCRIPTS_DIR / "config.txt"


def get_cookies() -> dict[str, str] | None:
    if not CONFIG_FILE.exists():
        print("config.txt not found — skipping puzzle download.")
        return

    session = CONFIG_FILE.read_text().strip()
    return {"session": session}


def parse_puzzle_title(year: int, day: int) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}"
    response = requests.get(url, cookies=get_cookies())

    if response.status_code != 200:
        print(f"Failed to parse puzzle title (HTTP {response.status_code})")
        return "TODO"

    soup = BeautifulSoup(response.text, features="html.parser")

    h2 = soup.find("h2")
    if h2 is None:
        print("Could not find puzzle title, leaving as TODO")
        return "TODO"

    match = re.match(rf"--- Day {day}: (?P<title>.*) ---", h2.get_text())
    if match is None:
        print("Failed to parse puzzle title, leaving as TODO")
        return "TODO"

    return match.group("title")


def download_example_input(year: int, day: int, dest_file: Path) -> None:
    url = f"https://adventofcode.com/{year}/day/{day}"
    response = requests.get(url, cookies=get_cookies())

    if response.status_code != 200:
        print(f"Failed to download example input (HTTP {response.status_code}), creating an empty file.")
        dest_file.write_text("")
        return

    soup = BeautifulSoup(response.text, features="html.parser")

    code_block = soup.find("code")
    if code_block is None:
        print("Could not find example puzzle input, creating an empty file.")
        dest_file.write_text("")
        return

    dest_file.write_text(code_block.get_text(strip=True))
    print(f"Downloaded example input: {dest_file.relative_to(PROJECT_ROOT)}")
    return


def download_puzzle_input(year: int, day: int, dest_file: Path) -> None:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = requests.get(url, cookies=get_cookies())

    if response.status_code != 200:
        print(f"Failed to download puzzle input (HTTP {response.status_code})")
        return

    dest_file.write_text(response.text.rstrip("\n"))
    print(f"Downloaded puzzle: {dest_file.relative_to(PROJECT_ROOT)}")
    return


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python scripts/create_day.py <year> <day>")
        sys.exit(1)

    year = int(sys.argv[1])
    day = int(sys.argv[2])

    target_dir = PROJECT_ROOT / f"aoc_{year}" / f"day_{day:02d}"
    target_dir.mkdir(parents=True, exist_ok=True)

    input_dir = target_dir / "input"
    input_dir.mkdir(parents=True, exist_ok=True)

    solution_file = target_dir / "solution.py"
    example_file = input_dir / "example.txt"
    puzzle_file = input_dir / "puzzle.txt"

    if solution_file.exists():
        print(f"{solution_file} already exists — not overwriting.")
    else:
        template = Template(TEMPLATE_FILE.read_text())
        template = template.substitute(YEAR=year, DAY=day, TITLE=parse_puzzle_title(year, day))
        solution_file.write_text(template)
        print(f"Created {solution_file.relative_to(PROJECT_ROOT)}")

    if example_file.exists() and example_file.read_text():
        print(f"{example_file} already exists and is non-empty — not overwriting.")
    else:
        download_example_input(year, day, example_file)

    if puzzle_file.exists() and puzzle_file.read_text():
        print(f"{puzzle_file} already exists and is non-empty — skipping download.")
    else:
        download_puzzle_input(year, day, puzzle_file)

    try:
        subprocess.run(["code", str(solution_file), str(example_file), str(puzzle_file)], check=False)
    except subprocess.SubprocessError:
        print("Failed to open files in VS Code")

    print("Done!")


if __name__ == "__main__":
    main()
