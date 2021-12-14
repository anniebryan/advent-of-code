from collections import deque

day = 11

# example_filename = f'day{day}/day{day}_ex.txt'
# example_input = open(example_filename).readlines()
# octopuses = [[int(val) for val in str(int(row))] for row in example_input]

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()
octopuses = [[int(val) for val in str(int(row))] for row in puzzle_input]

num_rows, num_cols = len(octopuses), len(octopuses[0])
num_octopuses = num_rows * num_cols

def get_octopus_dict():
  octopus_dict = {(i,j): octopuses[j][i] for i in range(num_cols) for j in range(num_rows)}
  return octopus_dict

def get_neighbors(i, j):
  left, right, up, down = ((i-1, j), (i+1, j), (i, j-1), (i, j+1))
  top_left, top_right, bottom_left, bottom_right = ((i-1, j-1), (i+1, j-1), (i-1, j+1), (i+1, j+1))
  locs = set()
  if i != 0:
    locs.add(left)
    if j != 0: locs.add(top_left)
    if j != num_rows-1: locs.add(bottom_left)

  if i != num_cols-1:
    locs.add(right)
    if j != 0: locs.add(top_right)
    if j != num_rows-1: locs.add(bottom_right)

  if j != 0: locs.add(up)
  if j != num_rows-1: locs.add(down)
  return locs

def timestep(d):
  new_d = d
  flashed = set()
  queue = deque()
  for loc in d:
    if d[loc] == 9:
      flashed.add(loc)
      for neighbor in get_neighbors(*loc):
        queue.append(neighbor)
    else:
      new_d[loc] = new_d[loc] + 1

  while queue:
    loc = queue.popleft()
    if loc not in flashed:
      if new_d[loc] == 9:
        flashed.add(loc)
        for neighbor in get_neighbors(*loc):
          queue.append(neighbor)
      else:
        new_d[loc] = new_d[loc] + 1
  
  for loc in flashed:
    new_d[loc] = 0

  return new_d, len(flashed)

def n_timesteps(d, n):
  total_flashed = 0
  for _ in range(n):
    d, num_flashed = timestep(d)
    total_flashed += num_flashed
  return total_flashed

def run_until_all_flashed(d):
  i = 0
  while True:
    i += 1
    d, num_flashed = timestep(d)
    if num_flashed == num_octopuses:
      return i

def part_1():
  octopus_dict = get_octopus_dict()
  return n_timesteps(octopus_dict, 100)

def part_2():
  octopus_dict = get_octopus_dict()
  return run_until_all_flashed(octopus_dict)

print(f'Part 1: {part_1()}')
print(f'Part 2: {part_2()}')
