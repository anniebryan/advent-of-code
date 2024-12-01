"""
Advent of Code 2020
Day 13: Shuttle Search
"""

from math import prod


def get_earliest_bus(puzzle_input):
    return int(puzzle_input[0])


def get_bus_times(puzzle_input):
    times = puzzle_input[1].split(',')
    return {int(x) for x in times if x != 'x'}


def next_bus_time(puzzle_input):
    earliest_bus = get_earliest_bus(puzzle_input)
    bus_times = get_bus_times(puzzle_input)
    time_to_wait = {x: x - earliest_bus % x for x in bus_times}
    soonest_bus = min(time_to_wait, key = time_to_wait.get)
    return soonest_bus, time_to_wait[soonest_bus]


def get_departure_requirements(puzzle_input):
    times = puzzle_input[1].split(',')
    return {(i, int(times[i])) for i in range(len(times)) if times[i] != 'x'}


def get_earliest_timestamp(puzzle_input):
    requirements = get_departure_requirements(puzzle_input)
    offsets = {(b - a % b, b) for a,b in requirements}
    time, inc = 0, 1
    for t, bus in offsets:
        while time % bus != t % bus:
            time += inc
        inc *= bus
    return time


def solve_part_1(puzzle_input: list[str]):
    return prod(next_bus_time(puzzle_input))


def solve_part_2(puzzle_input: list[str]):
    return get_earliest_timestamp(puzzle_input)
