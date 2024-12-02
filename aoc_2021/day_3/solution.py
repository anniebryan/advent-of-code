"""
Advent of Code 2021
Day 3: Binary Diagnostic
"""

import click
import os
import pathlib


def get_report(puzzle_input):
    return [n.split('\n')[0] for n in puzzle_input]


bits = lambda i, iterable: [int(n[i]) for n in iterable]
most_common = lambda i, iterable: '1' if sum(bits(i, iterable)) >= len(list(iterable)) / 2 else '0'
least_common = lambda i, iterable: '0' if sum(bits(i, iterable)) >= len(list(iterable)) / 2 else '1'

bin_to_dec = lambda bin: sum([2 ** i * int(bin[-i - 1]) for i in range(len(bin))])

remove = lambda i, fn, iterable: filter(lambda n: n[i] == fn(i, iterable), iterable)


def solve_part_1(puzzle_input: list[str]):
    report = get_report(puzzle_input)
    gamma_rate = ''.join([most_common(i, report) for i in range(len(report[0]))])
    epsilon_rate = ''.join([least_common(i, report) for i in range(len(report[0]))])
    return bin_to_dec(gamma_rate) * bin_to_dec(epsilon_rate)


def solve_part_2(puzzle_input: list[str]):
    report = get_report(puzzle_input)
    keep_most_common, keep_least_common = report, report
    
    for i in range(len(report[0])):
        temp_most = list(remove(i, most_common, keep_most_common))
        keep_most_common = temp_most if temp_most else keep_most_common

        temp_least = list(remove(i, least_common, keep_least_common))
        keep_least_common = temp_least if temp_least else keep_least_common
    
    return bin_to_dec(keep_most_common[0]) * bin_to_dec(keep_least_common[0])


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
