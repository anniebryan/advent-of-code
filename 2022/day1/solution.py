day = 1

example_filename = f'day{day}/example.txt
example_input = [r.strip() for r in open(example_filename).readlines()]

filename = f'day{day}/puzzle.txt'
puzzle_input = [r.strip() for r in open(filename).readlines()]

def get_max_three(a, b, c, current_elf):
  if current_elf > c:
    c = current_elf
    if current_elf > b:
      (b, c) = (current_elf, b)
      if current_elf > a:
        (a, b) = (current_elf, a)
  return (a, b, c)

def max_three_elves(input):
  a, b, c = 0, 0, 0
  current_elf = 0
  for cal in input:
    if cal == '':
      a, b, c = get_max_three(a, b, c, current_elf)
      current_elf = 0
    else:
      current_elf += int(cal)
  return get_max_three(a, b, c, current_elf)

def part_1(input):
  return max_three_elves(input)[0]

def part_2(input):
  return sum(max_three_elves(input))


print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
