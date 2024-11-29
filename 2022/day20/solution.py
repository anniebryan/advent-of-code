############################
# Advent of Code 2022 Day 20
############################

class LinkedList:
  def __init__(self, decryption_key):
    self.nodes = []
    self.length = 0
    self.first_node = None
    self.last_node = None
    self.zero_node = None
    self.decryption_key = decryption_key

  def add_node(self, val):
    node = Node(val * self.decryption_key)

    if self.first_node is None:
      self.first_node = node
      self.last_node = node

    if val == 0:
      self.zero_node = node

    node.link(self.first_node)
    self.last_node.link(node)

    self.last_node = node
    self.nodes.append(node)
    self.length += 1

  def move_node(self, node):
    num_spaces = node.val % (self.length - 1)
    if num_spaces != 0:
      p = node
      for _ in range(num_spaces):
        p = p.next
      node.prev.link(node.next)
      n = p.next
      p.link(node)
      node.link(n)

  def num_after_zero(self, num):
    i = num % self.length
    node = self.zero_node
    for _ in range(i):
      node = node.next
    return node.val


class Node:
  def __init__(self, val):
    self.val = val
    self.next = None
    self.prev = None

  def link(self, node):
    self.next = node
    node.prev = self


def parse(input, decryption_key):
  ls = LinkedList(decryption_key)
  for row in input:
    ls.add_node(int(row))
  return ls


def solve(input, decryption_key, num_times):
  ls = parse(input, decryption_key)
  nodes = ls.nodes
  for _ in range(num_times):
    for node in nodes:
      ls.move_node(node)
  return sum([ls.num_after_zero(i) for i in [1000, 2000, 3000]])


def part_1(input):
  return solve(input, 1, 1)
  
def part_2(input):
  return solve(input, 811589153, 10)

day = 20

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
