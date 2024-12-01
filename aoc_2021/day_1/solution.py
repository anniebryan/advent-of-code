"""
Advent of Code 2021
Day 1: Sonar Sweep
"""

def get_measurements(puzzle_input):
	return [int(n) for n in puzzle_input]


def increasing(x, y):
	return y > x


def three_sum(x, y, z):
	return x + y + z


def part_1(puzzle_input):
	measurements = get_measurements(puzzle_input)
	return sum(map(increasing, measurements, measurements[1:]))

def part_2(puzzle_input):
	measurements = get_measurements(puzzle_input)
	sums = list(map(three_sum, measurements, measurements[1:], measurements[2:]))
	return sum(map(increasing, sums, sums[1:]))
