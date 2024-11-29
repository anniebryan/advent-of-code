day = 2

example_filename = f'day{day}/example.txt'
example_input = open(example_filename).readlines()

filename = f'day{day}/puzzle.txt'
puzzle_input = open(filename).readlines()

def get_commands(input):
  return [(n.split(' ')[0], int(n.split(' ')[1])) for n in input]

forward = lambda x: x[0] == 'forward'
up = lambda x: x[0] == 'up'
down = lambda x: x[0] == 'down'
amount = lambda x: x[1]

def part_1(input):
  commands = get_commands(input)
  horiz = sum(map(amount, filter(forward, commands)))
  depth = sum(map(amount, filter(down, commands))) - sum(map(amount, filter(up, commands)))
  return horiz * depth

def part_2(input):
  commands = get_commands(input)
  horiz = sum(map(amount, filter(forward, commands)))
  depth, aim = 0, 0
  for x in commands:
    if forward(x):
      depth += aim*amount(x)
    elif down(x):
      aim += amount(x)
    elif up(x):
      aim -= amount(x)
  return horiz * depth


print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
