day = 12

example_filename = f'day{day}/day{day}_ex.txt'
example_input = [r.strip() for r in open(example_filename).readlines()]

filename = f'day{day}/day{day}.txt'
puzzle_input = [r.strip() for r in open(filename).readlines()]

def create_map(input):
  map = {}
  map_size = (0, 0)
  start_loc = None
  end_loc = None
  for i, row in enumerate(input):
    for j, val in enumerate(row):
      map_size = (max(map_size[0], i), max(map_size[1], j))
      if val == "S":
        start_loc = (i, j)
        map[(i, j)] = ord('a') - 96
      elif val == "E":
        end_loc = (i, j)
        map[(i, j)] = ord('z') - 96
      else:
        map[(i, j)] = ord(val) - 96
  return (map, map_size, start_loc, end_loc)

def is_valid_neighbor(map, map_size, current_height, neighbor):
  i, j = neighbor
  if 0 <= i <= map_size[0]:
    if 0 <= j <= map_size[1]:
      if current_height + 1 >= map[(i, j)]:
        return True
  return False

def bfs(map, map_size, start_loc, end_loc):
  queue = [start_loc]
  visited = {start_loc}
  dist = {start_loc: 0}

  while queue:
    loc = queue.pop(0)
    x, y = loc
    current_height = map[loc]

    for neighbor in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
      if is_valid_neighbor(map, map_size, current_height, neighbor):
        if neighbor not in visited:
          visited.add(neighbor)
          dist[neighbor] = dist[loc] + 1
          queue.append(neighbor)

          if neighbor == end_loc:
            return dist
  return None

def min_distances(map, map_size, start_locs, end_loc):
  for start_loc in start_locs:
    dist = bfs(map, map_size, start_loc, end_loc)
    if dist is not None:
      yield dist[end_loc]

def part_1(input):
  map, map_size, start_loc, end_loc = create_map(input)
  dist = bfs(map, map_size, start_loc, end_loc)
  if dist is not None:
    return dist[end_loc]
  return "Unable to get to E from S"

def part_2(input):
  map, map_size, _, end_loc = create_map(input)
  d = {}
  for start_loc in map:
    if map[start_loc] == 1: # valid start location
      dist = bfs(map, map_size, start_loc, end_loc)
      if dist is not None:
        d[start_loc] = dist[end_loc]

  if len(d) == 0:
    return "Unable to get to E from any square at elevation a"
  best_start_loc = min(d, key=d.get)
  return (best_start_loc, d[best_start_loc])

print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

example_sol = part_2(example_input)
print(f'Part 2 example: Starting from {example_sol[0]} gives a min distance of {example_sol[1]}')

puzzle_sol = part_2(puzzle_input)
print(f'Part 2 puzzle: Starting from {puzzle_sol[0]} gives a min distance of {puzzle_sol[1]}')
