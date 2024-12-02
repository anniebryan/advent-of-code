#!/usr/bin/env python3

import sys
import requests


def main(year: int, day: int) -> None:
    with open("config.txt") as config_file:
        session = config_file.readline().strip()
    response = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies={"session": session})
    with open(f"aoc_{year}/day_{day}/puzzle.txt", "w") as puzzle_file:
        puzzle_file.write(response.text.strip("\n"))


if __name__ == "__main__":
    year = int(sys.argv[1])
    day = int(sys.argv[2])
    main(year, day)
