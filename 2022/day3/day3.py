day = 3

example_filename = f'day{day}/day{day}_ex.txt'
example_input = open(example_filename).readlines()

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()

def letter_in_common_2(left, right):
  left_ch = set([ch for ch in left])
  for ch in right:
    if ch in left_ch:
      return ch

def letter_in_common_3(a, b, c):
  a_ch = set([ch for ch in a])
  b_ch = set([ch for ch in b])
  for ch in c:
    if ch in a_ch and ch in b_ch:
      return ch

def priority(ch):
  if 97 <= ord(ch) <= 122:
    return ord(ch) - 96
  else:
    return ord(ch) - 38

def part_1(input):
  tot = 0
  for row in input:
    row = row.strip()
    n = len(row)//2
    ch = letter_in_common_2(row[:n], row[n:])
    tot += priority(ch)
  return tot

def part_2(input):
  tot = 0
  for i in range(0, len(input), 3):
    ch = letter_in_common_3(*[row.strip() for row in input[i:i+3]])
    tot += priority(ch)
  return tot


print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
