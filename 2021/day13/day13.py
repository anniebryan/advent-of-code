day = 13

example_filename = f'day{day}/day{day}_ex.txt'
example_input = open(example_filename).readlines()

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()

def get_dots_instructions(input):
  dots, instructions = "".join(input).split('\n\n')
  dots = [tuple([int(val) for val in line.split(',')]) for line in dots.split('\n')]
  instructions = [tuple([line.split('=')[0][-1], int(line.split('=')[1])]) for line in instructions.split('\n')]
  return (dots, instructions)

def fold(dots, dir, val):
  new_dots = set()
  for dot in dots:
    x, y = dot
    if dir == 'x':
      new_x = x if val > x else 2*val - x
      new_dot = (new_x, y)
    else:
      new_y = y if val > y else 2*val - y
      new_dot = (x, new_y)
    new_dots.add(new_dot)
  return new_dots

def visualize(dots):
  max_x = max([dot[0] for dot in dots])
  max_y = max([dot[1] for dot in dots])

  s = '\n\n'
  for j in range(max_y + 1):
    s += ''.join(['#' if (i, j) in dots else '.' for i in range(max_x + 1)]) + '\n'
  return s

def part_1(input):
  (dots, instructions) = get_dots_instructions(input)
  dir, val = instructions[0]
  return len(fold(dots, dir, val))

def part_2(input):
  (dots, instructions) = get_dots_instructions(input)
  for instruction in instructions:
    dir, val = instruction
    dots = fold(dots, dir, val)
  return visualize(dots)


print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
