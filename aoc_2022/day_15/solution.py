"""
Advent of Code 2022
Day 15: Beacon Exclusion Zone
"""

import click
import os
import pathlib
import regex as re
from collections import defaultdict


def get_sensor_beacon_coordinates(puzzle_input):
    int_regex = "(-?\d+)"
    for row in puzzle_input:
        coordinates = re.match(f"Sensor at x={int_regex}, y={int_regex}: closest beacon is at x={int_regex}, y={int_regex}", row)
        (sensor_x, sensor_y, beacon_x, beacon_y) = map(int, coordinates.groups())
        yield (sensor_x, sensor_y, beacon_x, beacon_y)


def get_beacons(puzzle_input):
    beacons = defaultdict(set)
    for (_, _, beacon_x, beacon_y) in get_sensor_beacon_coordinates(puzzle_input):
        beacons[beacon_y].add(beacon_x)
    return beacons


def get_impossible_beacon_ranges(puzzle_input, verbose=False):
    # maps row -> list of tuples (a, b) where a beacon cannot exist in any of the points (a, row)...(b - 1, row)
    impossible_ranges = defaultdict(list)

    manhattan_distance = lambda x1, y1, x2, y2: abs(x1 - x2) + abs(y1 - y2)

    for i, (sensor_x, sensor_y, beacon_x, beacon_y) in enumerate(get_sensor_beacon_coordinates(puzzle_input)):
        if verbose:
            print(f"Row {i + 1}/{len(puzzle_input)}")

        d = manhattan_distance(sensor_x, sensor_y, beacon_x, beacon_y)
        for y in range(-d, d + 1):
            row = sensor_y + y
            max_x = d - abs(y)
            impossible_ranges[row].append((sensor_x - max_x, sensor_x + max_x + 1))

    return impossible_ranges


def find_impossible_positions(puzzle_input, row):
    impossible_ranges = get_impossible_beacon_ranges(puzzle_input)[row]
    beacons = get_beacons(puzzle_input)
    impossible_positions = set()

    for (a, b) in impossible_ranges:
        for i in range(a, b):
            if i not in beacons[row]:
                impossible_positions.add(i)

    return impossible_positions


def find_remaining_sensor(puzzle_input, max_to_search):
    impossible_ranges = get_impossible_beacon_ranges(puzzle_input)
    for i in range(max_to_search + 1):
        sorted_ranges = sorted(impossible_ranges[i], key=lambda r: r[0])
        max_found = sorted_ranges[0][1]
        for j in range(len(sorted_ranges) - 1):
            range_1 = sorted_ranges[j]
            range_2 = sorted_ranges[j + 1]
            if range_2[0] > max_found:
                return (range_1[1], i)
            max_found = max(max_found, range_2[1])


def solve_part_1(puzzle_input: list[str]):
    row = int(puzzle_input[0])
    return len(find_impossible_positions(puzzle_input[2:], row))


def solve_part_2(puzzle_input: list[str]):
    max_to_search = int(puzzle_input[1])
    x, y = find_remaining_sensor(puzzle_input[2:], max_to_search)
    return x * 4000000 + y


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
