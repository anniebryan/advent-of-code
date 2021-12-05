day = 1
filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()
measurements = [int(n) for n in puzzle_input]

example = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
# measurements = example

increasing = lambda x, y: y > x

def part_1():
  return sum(map(increasing, measurements, measurements[1:]))

def part_2():
  three_sum = lambda x, y, z: x + y + z
  sums = list(map(three_sum, measurements, measurements[1:], measurements[2:]))
  return sum(map(increasing, sums, sums[1:]))

print(f'Part 1: {part_1()}')
print(f'Part 2: {part_2()}')
