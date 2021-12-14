from functools import reduce

day = 9

# example_filename = f'day{day}/day{day}_ex.txt'
# example_input = open(example_filename).readlines()
# heightmap = [[int(val) for val in str(int(row))] for row in example_input]

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()
heightmap = [[int(val) for val in row.strip()] for row in puzzle_input]

num_rows, num_cols = len(heightmap), len(heightmap[0])
heightmap_dict = {(i,j): heightmap[j][i] for i in range(num_cols) for j in range(num_rows)}

def horizontal_neighbor_locs(i, j):
  left, right = ((i-1, j), (i+1, j))
  locs = set()
  if i != 0: locs.add(left)
  if i != num_cols-1: locs.add(right)
  return locs

def vertical_neighbor_locs(i, j):
  up, down = ((i, j-1), (i, j+1))
  locs = set()
  if j != 0: locs.add(up)
  if j != num_rows-1: locs.add(down)
  return locs

def neighbor_locs(i, j):
  return horizontal_neighbor_locs(i, j).union(vertical_neighbor_locs(i, j))

def is_low_point(i, j):
  val = heightmap_dict[(i, j)]
  neighbors = neighbor_locs(i, j)
  neighbor_vals = [heightmap_dict[n] for n in neighbors]
  return all(list(map(lambda v: val < v, neighbor_vals)))

def expand_basin_horizontally(i, j):
  basin = {(i, j)}
  val = heightmap_dict[(i, j)]
  neighbors = horizontal_neighbor_locs(i, j)
  add_to_basin = set(filter(lambda v: val < heightmap_dict[v] and heightmap_dict[v] != 9, neighbors))
  if add_to_basin:
    expanded = set()
    for loc in add_to_basin:
      expanded = expanded.union(expand_basin_horizontally(*loc))
    basin = basin.union(expanded)
  return basin

def expand_basin_vertically(i, j):
  basin = {(i, j)}
  val = heightmap_dict[(i, j)]
  neighbors = vertical_neighbor_locs(i, j)
  add_to_basin = set(filter(lambda v: val < heightmap_dict[v] and heightmap_dict[v] != 9, neighbors))
  basin = basin.union(add_to_basin)
  return basin

def create_basin(i, j):
  basin = expand_basin_horizontally(i, j)
  original_size = len(basin)
  finished = False

  while not finished:
    # expand vertically
    basin = basin.union(*[expand_basin_vertically(*loc) for loc in basin])

    # expand horizontally
    basin = basin.union(*[expand_basin_horizontally(*loc) for loc in basin])

    new_size = len(basin)
    finished = (new_size == original_size)
    original_size = new_size
  return basin

def basin_size(i, j):
  return len(create_basin(i, j))

def get_low_points():
  return list(filter(lambda loc: is_low_point(*loc), heightmap_dict.keys()))

def part_1():
  return sum(list(map(lambda loc: 1+heightmap_dict[loc], get_low_points())))

def part_2():
  basin_sizes = map(lambda loc: basin_size(*loc), get_low_points())
  return reduce(lambda a, b: a*b, sorted(basin_sizes, reverse=True)[:3])

print(f'Part 1: {part_1()}')
print(f'Part 2: {part_2()}')
