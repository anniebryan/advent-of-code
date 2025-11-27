"""
Advent of Code 2018
Day 4: Repose Record
"""

import click
import os
import pathlib
import regex as re
from collections import defaultdict


def parse_records(puzzle_input):
    pattern = r'\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.+)'
    records = [re.match(pattern, row).groups() for row in puzzle_input]

    total_minutes = defaultdict(int)  # maps guard ID --> total minutes asleep
    ind_minutes = defaultdict(lambda: defaultdict(int))  # maps guard ID --> minute --> instances asleep

    for line in sorted(records):
        if 'Guard' in line[5]:
            guard_id = int(re.findall(r'\d+', line[5])[0])
        elif 'asleep' in line[5]:
            min_0 = int(line[4])
        elif 'wakes' in line[5]:
            min_1 = int(line[4])
            total_minutes[guard_id] += min_1 - min_0
            for m in range(min_0, min_1):
                ind_minutes[guard_id][m] += 1

    return total_minutes, ind_minutes


def solve_part_1(puzzle_input: list[str]):
    total_minutes, ind_minutes = parse_records(puzzle_input)
    max_guard = max(total_minutes, key = total_minutes.get)  # guard who sleeps the most
    max_minute = max(ind_minutes[max_guard], key = ind_minutes[max_guard].get)
    return f"{max_guard} * {max_minute} = {max_guard * max_minute}"


def solve_part_2(puzzle_input: list[str]):
    _, ind_minutes = parse_records(puzzle_input)
    common_minutes = {}
    for guard in ind_minutes:
        most_common_minute = max(ind_minutes[guard], key = ind_minutes[guard].get)
        time_at_minute = ind_minutes[guard][most_common_minute]  # number of times guard was asleep during that minute
        common_minutes[guard] = (most_common_minute, time_at_minute)
    final_guard = max(common_minutes, key = lambda x: common_minutes[x][1])
    final_minute = common_minutes[final_guard][0]
    return f"{final_guard} * {final_minute} = {final_guard * final_minute}"


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
