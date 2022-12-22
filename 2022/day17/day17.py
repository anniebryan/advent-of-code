from collections import deque
from itertools import cycle

############################
# Advent of Code 2022 Day 17
############################

def get_rocks():
  # in a function rather than a constant so that cycle resets after each call
  return cycle([
    [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 2, 'y': 0}, {'x': 3, 'y': 0}],
    [{'x': 1, 'y': 0}, {'x': 0, 'y': 1}, {'x': 1, 'y': 1}, {'x': 2, 'y': 1}, {'x': 1, 'y': 2}],
    [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 2, 'y': 0}, {'x': 2, 'y': 1}, {'x': 2, 'y': 2}],
    [{'x': 0, 'y': 0}, {'x': 0, 'y': 1}, {'x': 0, 'y': 2}, {'x': 0, 'y': 3}],
    [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 0, 'y': 1}, {'x': 1, 'y': 1}]
  ])


def can_move_horizontal(rock: list[dict], dx: int, ground: set[tuple]):
  for d in rock:
    x, y = d['x'], d['y']
    if not(0 <= x + dx <= 6):
      return False
    if (x + dx, y) in ground:
      return False
  return True


def can_drop(rock: list[dict], ground: set[tuple]):
  for d in rock:
    x, y = d['x'], d['y']
    if (x, y - 1) in ground:
      return False
  return True


def drop(rock: list[dict], ground: set[tuple], jet_queue: cycle):
  while True:
    j = jet_queue.__next__()
    dx = {"<": -1, ">": 1}[j]
    if can_move_horizontal(rock, dx, ground):
      for d in rock:
        d['x'] += dx
    if can_drop(rock, ground):
      for d in rock:
        d['y'] -= 1
    else:
      break


def drop_n_rocks(jet_queue, n):
  rocks = get_rocks()
  height = 0
  ground = set([(i, 0) for i in range(7)])
  for _ in range(n):
    rock = [{'x': d['x'] + 2, 'y': d['y'] + height + 4} for d in rocks.__next__()]
    drop(rock, ground, jet_queue)
    ground.update((d['x'], d['y']) for d in rock)
    height = max(height, max(d['y'] for d in rock))
  return height

def part_1(input):
  jet_queue = cycle(input[0])
  return drop_n_rocks(jet_queue, 2022)

def part_2(input):
  jet_queue = cycle(input[0])
  # TODO too slow, need to optimize
  return drop_n_rocks(jet_queue, 1000000000000)


day = 17


with open(f'day{day}/day{day}_ex.txt') as ex_filename:
  example_input = [r.strip() for r in ex_filename.readlines()]
  print("---Example---")
  print(f'Part 1: {part_1(example_input)}')
  # print(f'Part 2: {part_2(example_input)}')

with open(f'day{day}/day{day}.txt') as filename:
  puzzle_input = [r.strip() for r in filename.readlines()]
  print("---Puzzle---")
  print(f'Part 1: {part_1(puzzle_input)}')
  # print(f'Part 2: {part_2(puzzle_input)}')
