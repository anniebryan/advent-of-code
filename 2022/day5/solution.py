from collections import defaultdict
import re

day = 5

example_filename = f'day{day}/day{day}_ex.txt'
example_input = open(example_filename).readlines()

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()

def get_crates_and_instructions(input):
  crates = defaultdict(list)
  instructions = []
  is_instruction = False
  for row in input:
    if row == '\n':
      is_instruction = True # switch
    elif is_instruction:
      items = row.split(" ")
      instructions.append(tuple([int(items[i]) for i in [1,3,5]]))
    else: # crate
      for i, ch in enumerate(row):
        if i % 4 == 1 and ch != ' ' and not re.match('\d+', ch):
          crates[(i // 4) + 1].append(ch)
  crates = {i: crates[i][::-1] for i in crates}
  return crates, instructions

def execute_instruction(instruction, crates, part_2):
  (a, b, c) = instruction
  elems = [crates[b].pop() for _ in range(a)]
  if part_2:
    elems = elems[::-1]
  for elem in elems:
    crates[c].append(elem)
  return crates

def execute_instructions(input, part_2):
  crates, instructions = get_crates_and_instructions(input)
  for instruction in instructions:
    crates = execute_instruction(instruction, crates, part_2)
  return crates

def topmost_crates(crates):
  topmost = [crates[i][-1] for i in sorted(crates.keys())]
  return "".join(topmost)

def part_1(input):
  crates = execute_instructions(input, False)
  return topmost_crates(crates)

def part_2(input):
  crates = execute_instructions(input, True)
  return topmost_crates(crates)


print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
