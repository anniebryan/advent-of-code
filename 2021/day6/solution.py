"""
Advent of Code 2021
Day 6: Lanternfish
"""

from collections import defaultdict

def get_initial_timers(puzzle_input):
    timers = defaultdict(int)
    for val in puzzle_input[0].split(','):
        timers[int(val)] += 1
    return timers

def simulate_day(timers):
    new_timers = {key-1: val for key, val in timers.items() if key != 0}
    if 0 in timers:
        new_timers[6] = new_timers[6] + timers[0] if 6 in new_timers else timers[0]
        new_timers[8] = new_timers[8] + timers[0] if 8 in new_timers else timers[0]
    return new_timers
    
def simulate_n_days(puzzle_input, n):
    timers = get_initial_timers(puzzle_input)
    for _ in range(n):
        timers = simulate_day(timers)
    return timers

def part_1(puzzle_input):
    return sum(simulate_n_days(puzzle_input, 80).values())

def part_2(puzzle_input):
    return sum(simulate_n_days(puzzle_input, 256).values())
