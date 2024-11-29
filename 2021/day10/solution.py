from collections import deque
from statistics import median

day = 10

example_filename = f'day{day}/day{day}_ex.txt'
example_input = open(example_filename).readlines()

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()

def get_lines(input):
  return [line.strip() for line in input]

table = {')': 3, ']': 57, '}': 1197, '>': 25137}
points = {')': 1, ']': 2, '}': 3, '>': 4}
opening_chars = {'(', '[', '{', '<'}
closing_chars = {'(': ')', '[': ']', '{': '}', '<': '>'}

def find_first_illegal_char(line):
  chars = deque()
  for s in line:
    if s in opening_chars:
      chars.append(closing_chars[s])
    else:
      expected = chars.pop()
      if s != expected:
        return s

def fill_incomplete(line):
  chars = deque()
  for s in line:
    if s in opening_chars:
      chars.append(closing_chars[s])
    else:
      expected = chars.pop()
      if s != expected:
        return None # corrupted line
  completion_string = ''
  while chars:
    completion_string += chars.pop()
  return completion_string

def get_score(completion_string):
  score = 0
  for s in completion_string:
    score *= 5
    score += points[s]
  return score

def part_1(input):
  lines = get_lines(input)
  return sum([table[find_first_illegal_char(line)] for line in lines if find_first_illegal_char(line) is not None])

def part_2(input):
  lines = get_lines(input)
  return median([get_score(fill_incomplete(line)) for line in lines if fill_incomplete(line) is not None])
      

print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
