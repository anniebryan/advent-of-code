from collections import defaultdict, deque

day = 12

# example_filename = f'day{day}/day{day}_ex.txt'
# example_input = open(example_filename).readlines()
# edges = set([tuple([s.strip() for s in line.split('-')]) for line in example_input])

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()
edges = set([tuple([s.strip() for s in line.split('-')]) for line in puzzle_input])

is_end = lambda s: s == 'end'
is_small = lambda s: s.islower() and not is_end(s)

neighbors = defaultdict(set)

for edge in edges:
  x, y = edge
  if x != 'start':
    neighbors[y].add(x)
  if y != 'start':
    neighbors[x].add(y)

def cave_generator(part_2):
  paths = deque()
  start_path = (['start'], 'start', set(), None)
  paths.append(start_path)

  while paths:
    current = paths.popleft()
    path, most_recent, small_caves_visited, small_cave_visited_twice = current

    for neighbor in neighbors[most_recent]:
      new_path = path + [neighbor]
      if is_end(neighbor):
        yield new_path
      elif is_small(neighbor):
        new_small_caves_visited = small_caves_visited.union({neighbor})
        if part_2:
          if small_cave_visited_twice is None:
            new_small_cave_visited_twice = neighbor if neighbor in small_caves_visited else None
            paths.append((new_path, neighbor, new_small_caves_visited, new_small_cave_visited_twice))
          elif neighbor != small_cave_visited_twice and neighbor not in small_caves_visited:
            paths.append((new_path, neighbor, new_small_caves_visited, small_cave_visited_twice))
        elif neighbor not in small_caves_visited:
          paths.append((new_path, neighbor, new_small_caves_visited, None))
      else:
        paths.append((new_path, neighbor, small_caves_visited, small_cave_visited_twice))

def part_1():
  return len([path for path in cave_generator(False)])

def part_2():
  return len([path for path in cave_generator(True)])

print(f'Part 1: {part_1()}')
print(f'Part 2: {part_2()}')
