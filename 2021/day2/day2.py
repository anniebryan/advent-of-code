day = 2
filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()
commands = [(n.split(' ')[0], int(n.split(' ')[1])) for n in puzzle_input]

example = [('forward', 5), ('down', 5), ('forward', 8), ('up', 3), ('down', 8), ('forward', 2)]
# commands = example

forward = lambda x: x[0] == 'forward'
up = lambda x: x[0] == 'up'
down = lambda x: x[0] == 'down'

amount = lambda x: x[1]

def part_1():
  horiz = sum(map(amount, filter(forward, commands)))
  depth = sum(map(amount, filter(down, commands))) - sum(map(amount, filter(up, commands)))
  return horiz * depth

def part_2():
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

print(f'Part 1: {part_1()}')
print(f'Part 2: {part_2()}')
