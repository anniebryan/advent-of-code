day = 1

example_filename = f'day{day}/day{day}_ex.txt'
example_input = open(example_filename).readlines()

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()

def get_all_elves():
  elf_cals = []
  for cal in puzzle_input:
    if cal != '\n':
      elf_cals.append(int(cal))
    else:
      yield sum(elf_cals)
      elf_cals = []
  yield sum(elf_cals)

def part_1():
  return max(get_all_elves())

def part_2():
  return sum(sorted(get_all_elves(), reverse=True)[:3])

print(f'Part 1: {part_1()}')
print(f'Part 2: {part_2()}')
