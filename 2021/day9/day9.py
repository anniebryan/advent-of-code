from functools import reduce

day = 9

example_filename = f'day{day}/day{day}_ex.txt'
example_input = open(example_filename).readlines()

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()

def get_heightmap_dict(input):
  heightmap = [[int(val) for val in row.strip()] for row in input]
  num_rows = len(heightmap)
  num_cols = len(heightmap[0])
  heightmap_dict = {(i,j): heightmap[j][i] for i in range(num_cols) for j in range(num_rows)}
  return (heightmap_dict, num_rows, num_cols)

def horizontal_neighbor_locs(num_cols, i, j):
  left, right = ((i - 1, j), (i + 1, j))
  locs = set()
  if i != 0:
    locs.add(left)
  if i != num_cols-1:
    locs.add(right)
  return locs

def vertical_neighbor_locs(num_rows, i, j):
  up, down = ((i, j-1), (i, j+1))
  locs = set()
  if j != 0:
    locs.add(up)
  if j != num_rows-1:
    locs.add(down)
  return locs

def is_low_point(heightmap_dict, num_rows, num_cols, i, j):
  val = heightmap_dict[(i, j)]
  neighbors = horizontal_neighbor_locs(num_cols, i, j).union(vertical_neighbor_locs(num_rows, i, j))
  return all([val < heightmap_dict[n] for n in neighbors])

def expand_basin_horizontally(heightmap_dict, num_cols, i, j):
  basin = {(i, j)}
  val = heightmap_dict[(i, j)]
  neighbors = horizontal_neighbor_locs(num_cols, i, j)
  add_to_basin = {v for v in neighbors if val < heightmap_dict[v] and heightmap_dict[v] != 9}
  for loc in add_to_basin:
    basin = basin.union(expand_basin_horizontally(heightmap_dict, num_cols, *loc))
  return basin

def expand_basin_vertically(heightmap_dict, num_rows, i, j):
  basin = {(i, j)}
  val = heightmap_dict[(i, j)]
  neighbors = vertical_neighbor_locs(num_rows, i, j)
  add_to_basin = {v for v in neighbors if val < heightmap_dict[v] and heightmap_dict[v] != 9}
  basin = basin.union(add_to_basin)
  return basin

def create_basin(heightmap_dict, num_rows, num_cols, i, j):
  basin = expand_basin_horizontally(heightmap_dict, num_cols, i, j)
  prev_size = len(basin)
  finished = False

  while not finished:
    expand_vertically = [expand_basin_vertically(heightmap_dict, num_rows, *loc) for loc in basin]
    basin = basin.union(*expand_vertically)

    expand_horizontally = [expand_basin_horizontally(heightmap_dict, num_cols, *loc) for loc in basin]
    basin = basin.union(*expand_horizontally)

    new_size = len(basin)
    finished = (new_size == prev_size)
    prev_size = new_size

  return basin

def get_low_points(heightmap_dict, num_rows, num_cols):
  return [loc for loc in heightmap_dict.keys() if is_low_point(heightmap_dict, num_rows, num_cols, *loc)]

def part_1(input):
  (heightmap_dict, num_rows, num_cols) = get_heightmap_dict(input)
  low_points = get_low_points(heightmap_dict, num_rows, num_cols)
  return sum([1 + heightmap_dict[loc] for loc in low_points])

def part_2(input):
  (heightmap_dict, num_rows, num_cols) = get_heightmap_dict(input)
  low_points = get_low_points(heightmap_dict, num_rows, num_cols)
  basin_sizes = [len(create_basin(heightmap_dict, num_rows, num_cols, *loc)) for loc in low_points]
  three_largest_basins = sorted(basin_sizes, reverse=True)[:3]
  return reduce(lambda a, b: a * b, three_largest_basins)


print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
