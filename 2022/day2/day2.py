day = 2

example_filename = f'day{day}/day{day}_ex.txt'
example_input = open(example_filename).readlines()

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()

def opponent_move(a):
  return {"A": 0, "B": 1, "C": 2}[a]

def my_move(a, b, part_1):
  if part_1:
    return {"X": 0, "Y": 1, "Z": 2}[b]
  else:
    opp = opponent_move(a)
    return (opp + {"X": -1, "Y": 0, "Z": 1}[b]) % 3

def move_score(a, b, part_1):
  val = my_move(a, b, part_1)
  return val + 1

def outcome_score(a, b, part_1):
  if part_1:
    me = my_move(a, b, True)
    opp = opponent_move(a)
    difference = (me - opp) % 3
    return 3*((difference + 1) % 3)
  return {"X": 0, "Y": 3, "Z": 6}[b]

def get_score(row, part_1):
  a, b = [c.strip() for c in row.split(" ")]
  return move_score(a, b, part_1) + outcome_score(a, b, part_1)

def part_1(input):
  return sum([get_score(row, True) for row in input])

def part_2(input):
  return sum([get_score(row, False) for row in input])

print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
