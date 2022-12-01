day = 1

example_filename = f'day{day}/day{day}_ex.txt'
example_input = open(example_filename).readlines()

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()

def get_all_elves(input):
  elf_cals = []
  for cal in input:
    if cal != '\n':
      elf_cals.append(int(cal))
    else:
      yield sum(elf_cals)
      elf_cals = []
  yield sum(elf_cals)

def part_1(input):
  return max(get_all_elves(input))

def part_2(input):
  return sum(sorted(get_all_elves(input), reverse=True)[:3])

print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
