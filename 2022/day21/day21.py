############################
# Advent of Code 2022 Day 21
############################

import re
import operator

class Monkey:
  def __init__(self, row):
    match = re.match(f"(.*): (\d+)", row)
    if match is not None:
      (name, number) = match.groups()
      self.name = name
      self.number = int(number)
      self.monkey_one = None
      self.operation = None
      self.monkey_two = None
    else:
      match = re.match(f"(.*): (.*) (\+|\-|\*|\/) (.*)", row)
      assert(match is not None)
      (name, monkey_one, operation, monkey_two) = match.groups()
      self.name = name
      self.number = None
      self.monkey_one = monkey_one
      self.operation = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}[operation]
      self.monkey_two = monkey_two

  def know_number(self):
    return self.number is not None


def parse(input):
  monkeys = {}
  known_numbers = {}
  for row in input:
    monkey = Monkey(row)
    monkeys[monkey.name] = monkey
    if monkey.know_number():
      known_numbers[monkey.name] = monkey.number
  return monkeys, known_numbers

def part_1(input):
  monkeys, known_numbers = parse(input)
  while "root" not in known_numbers:
    for name, monkey in monkeys.items():
      if name not in known_numbers:
        monkey_one = monkey.monkey_one
        monkey_two = monkey.monkey_two
        if monkey_one in known_numbers and monkey_two in known_numbers:
          monkey_num = monkey.operation(known_numbers[monkey_one], known_numbers[monkey_two])
          monkey.number = monkey_num
          known_numbers[name] = monkey_num
  return int(known_numbers["root"])

  
def part_2(input):
  return "Not implemented"


day = 21

with open(f'day{day}/day{day}_ex.txt') as ex_filename:
  example_input = [r.strip() for r in ex_filename.readlines()]
  print("---Example---")
  print(f'Part 1: {part_1(example_input)}')
  print(f'Part 2: {part_2(example_input)}')

with open(f'day{day}/day{day}.txt') as filename:
  puzzle_input = [r.strip() for r in filename.readlines()]
  print("---Puzzle---")
  print(f'Part 1: {part_1(puzzle_input)}')
  print(f'Part 2: {part_2(puzzle_input)}')
