from collections import defaultdict

day = 5

# example_filename = f'day{day}/day{day}_ex.txt'
# example_input = open(example_filename).readlines()
# example_point_pairs = [tuple([tuple([int(val) for val in point.split(',')]) for point in line.split(' -> ')]) for line in example_input]

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()
point_pairs = [tuple([tuple([int(val) for val in point.split(',')]) for point in line.split(' -> ')]) for line in puzzle_input]

def generate_diagram(diagonals):
  diagram = defaultdict(int)
  for point_pair in point_pairs:
    ((x1, y1), (x2, y2)) = point_pair
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)
    if x1 == x2: # horizontal
      for y in range(min_y, max_y+1):
        diagram[(x1, y)] += 1
    elif y1 == y2: # vertical
      for x in range(min_x, max_x+1):
        diagram[(x, y1)] += 1
    elif diagonals: # diagonal
      if (x1 == max_x and y1 == max_y) or (x2 == max_x and y2 == max_y):
        for i in range(max_x-min_x+1):
          diagram[(min_x+i, min_y+i)] += 1
      else:
        for i in range(max_x-min_x+1):
          diagram[(min_x+i, max_y-i)] += 1
  return diagram

def part_1():
  diagram = generate_diagram(False)
  return len([key for key in diagram if diagram[key] >= 2])

def part_2():
  diagram = generate_diagram(True)
  return len([key for key in diagram if diagram[key] >= 2])

print(f'Part 1: {part_1()}')
print(f'Part 2: {part_2()}')
