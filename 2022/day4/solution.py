day = 4

example_filename = f'day{day}/example.txt
example_input = [r.strip() for r in open(example_filename).readlines()]

filename = f'day{day}/puzzle.txt'
puzzle_input = [r.strip() for r in open(filename).readlines()]

def get_sections(input):
  for r in input:
    elf_one, elf_two = r.split(',')
    a, b = elf_one.split('-')
    c, d = elf_two.split('-')
    yield (int(a), int(b), int(c), int(d))

def part_1(input):
  num_overlap = 0
  for (a, b, c, d) in get_sections(input):
    if a <= c <= d <= b:
      num_overlap += 1
    elif c <= a <= b <= d:
      num_overlap += 1
  return num_overlap

def part_2(input):
  num_overlap = 0
  for (a, b, c, d) in get_sections(input):
    if a <= c <= b:
      num_overlap += 1
    elif c <= a <= d:
      num_overlap += 1
  return num_overlap


print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
