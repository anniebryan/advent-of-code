day = 7

example_filename = f'day{day}/day{day}_ex.txt'
example_input = open(example_filename).readlines()

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()

def get_positions(input):
  return [int(val) for val in input[0].split(',')]

def min_distance(input, distance_fn):
  positions = get_positions(input)
  return min([distance_fn(i, positions) for i in range(max(positions))])

def part_1(input):
  abs_distance = lambda i, positions: int(sum([abs(p-i) for p in positions]))
  return min_distance(input, abs_distance)

def part_2(input):
  distance = lambda i, positions: int(sum([abs(p-i)*(abs(p-i)+1)/2 for p in positions]))
  return min_distance(input, distance)


print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
