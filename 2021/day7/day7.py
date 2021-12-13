# from statistics import median

day = 7

# example_filename = f'day{day}/day{day}_ex.txt'
# example_input = open(example_filename).readlines()
# positions = [int(val) for val in example_input[0].split(',')]

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()
positions = [int(val) for val in puzzle_input[0].split(',')]

abs_distance = lambda i: int(sum([abs(p-i) for p in positions]))
distance = lambda i: int(sum([abs(p-i)*(abs(p-i)+1)/2 for p in positions]))

def part_1():
  # return int(sum([abs(p-median(positions)) for p in positions]))
  return min([abs_distance(i) for i in range(max(positions))])

def part_2():
  return min([distance(i) for i in range(max(positions))])

print(f'Part 1: {part_1()}')
print(f'Part 2: {part_2()}')
