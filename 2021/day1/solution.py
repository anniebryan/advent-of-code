def get_measurements(puzzle_input):
	return [int(n) for n in puzzle_input]

increasing = lambda x, y: y > x
three_sum = lambda x, y, z: x + y + z

def part_1(puzzle_input):
	measurements = get_measurements(puzzle_input)
	return sum(map(increasing, measurements, measurements[1:]))

def part_2(puzzle_input):
	measurements = get_measurements(puzzle_input)
	sums = list(map(three_sum, measurements, measurements[1:], measurements[2:]))
	return sum(map(increasing, sums, sums[1:]))
