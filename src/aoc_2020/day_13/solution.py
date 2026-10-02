"""
Advent of Code 2020
Day 13: Shuttle Search
"""

from math import prod


def parse_input(puzzle_input: list[str]) -> tuple[int, set[int], set[tuple[int, int]]]:
    earliest_bus = int(puzzle_input[0])

    times = puzzle_input[1].split(',')
    bus_times = {int(x) for x in times if x != 'x'}

    departure_requirements = {(i, int(times[i])) for i in range(len(times)) if times[i] != 'x'}

    return earliest_bus, bus_times, departure_requirements


def next_bus_time(earliest_bus, bus_times):
    time_to_wait = {x: x - earliest_bus % x for x in bus_times}
    min_time = min(time_to_wait.values())
    for k, v in time_to_wait.items():
        if v == min_time:
            return k, min_time
    raise AssertionError


def get_earliest_timestamp(requirements):
    offsets = {(b - a % b, b) for a,b in requirements}
    time, inc = 0, 1
    for t, bus in offsets:
        while time % bus != t % bus:
            time += inc
        inc *= bus
    return time


def solve_part_1(puzzle_input: list[str]):
    earliest_bus, bus_times, _ = parse_input(puzzle_input)
    return prod(next_bus_time(earliest_bus, bus_times))


def solve_part_2(puzzle_input: list[str]):
    _, _, requirements = parse_input(puzzle_input)
    return get_earliest_timestamp(requirements)
