day = 6

example_filename = f'day{day}/example.txt'
example_input = open(example_filename).readlines()[0]

filename = f'day{day}/puzzle.txt'
puzzle_input = open(filename).readlines()[0]

def all_different(last_elems):
  return len(last_elems) == len(set(last_elems))

def find_marker(input, n):
  last_n = tuple(input[:n])
  for i, ch in enumerate(input[n:]):
    if all_different(last_n):
      return i + n
    else:
      last_n = last_n[1:] + (ch,)

def part_1(input):
  return find_marker(input, 4)

def part_2(input):
  return find_marker(input, 14)


print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
