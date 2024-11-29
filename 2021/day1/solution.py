day = 1

example_filename = f'day{day}/example.txt'
example_input = open(example_filename).readlines()

filename = f'day{day}/puzzle.txt'
puzzle_input = open(filename).readlines()

def get_measurements(input):
  return [int(n) for n in input]

increasing = lambda x, y: y > x
three_sum = lambda x, y, z: x + y + z

def part_1(input):
  measurements = get_measurements(input)
  return sum(map(increasing, measurements, measurements[1:]))

def part_2(input):
  measurements = get_measurements(input)
  sums = list(map(three_sum, measurements, measurements[1:], measurements[2:]))
  return sum(map(increasing, sums, sums[1:]))


print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
