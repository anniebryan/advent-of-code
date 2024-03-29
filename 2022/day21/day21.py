############################
# Advent of Code 2022 Day 21
############################

import re
import operator

ops = {
  "+": operator.add,
  "-": operator.sub,
  "*": operator.mul,
  "/": operator.truediv
}

inverse_ops = {
  "+": operator.sub,
  "-": operator.add,
  "*": operator.truediv,
  "/": operator.mul
}


class Monkey:
  def __init__(self, row):
    match = re.match(f"(.*): (\d+)", row)
    if match is not None:
      (name, number) = match.groups()
      self.name = name
      self.number = int(number)
    else:
      match = re.match(f"(.*): (.*) (\+|\-|\*|\/) (.*)", row)
      assert(match is not None)
      (name, monkey_one, operation, monkey_two) = match.groups()
      self.name = name
      self.number = None
      self.monkey_one_name = monkey_one
      self.monkey_two_name = monkey_two
      self.operation = operation

  def get_number(self, monkeys):
    if self.number is not None:
      return self.number

    left_val = monkeys[self.monkey_one_name].get_number(monkeys)
    right_val = monkeys[self.monkey_two_name].get_number(monkeys)

    if isinstance(left_val, int) and isinstance(right_val, int):
      return int(ops[self.operation](left_val, right_val))
    else:
      return Expression(left_val, right_val, self.operation)

class Expression:
  def __init__(self, left, right, operation):
    self.left = left
    self.right = right
    self.op_symbol = operation

  def __str__(self):
    return f"({self.left} {self.op_symbol} {self.right})"


def parse(input):
  monkeys = {}
  for row in input:
    monkey = Monkey(row)
    monkeys[monkey.name] = monkey
  return monkeys

def set_equal(monkeys):
  root_monkey = monkeys["root"]
  monkeys["humn"].number = "X"
  target_value = monkeys[root_monkey.monkey_two_name].get_number(monkeys)
  expression = monkeys[root_monkey.monkey_one_name].get_number(monkeys)
  while not ((isinstance(expression, str)) or isinstance(expression.left, int) and isinstance(expression.right, int)):
    if isinstance(expression.right, int):
      target_value = int(inverse_ops[expression.op_symbol](target_value, expression.right))
      expression = expression.left
    elif isinstance(expression.left, int):
      if expression.op_symbol in {"+", "*"}:
        target_value = int(inverse_ops[expression.op_symbol](target_value, expression.left))
      else:
        target_value = int(ops[expression.operation](expression.left, target_value))
      expression = expression.right
  return target_value


def part_1(input):
  monkeys = parse(input)
  return monkeys["root"].get_number(monkeys)

  
def part_2(input):
  monkeys = parse(input)
  return set_equal(monkeys)


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
