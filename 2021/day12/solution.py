"""
Advent of Code 2021
Day 12: Passage Pathing
"""

from collections import defaultdict, deque

def get_edges(puzzle_input):
    return {tuple([s.strip() for s in line.split('-')]) for line in puzzle_input}

is_end = lambda s: s == 'end'
is_small = lambda s: s.islower() and not is_end(s)

def get_neighbors(puzzle_input):
    neighbors = defaultdict(set)
    for edge in get_edges(puzzle_input):
        x, y = edge
        if x != 'start':
            neighbors[y].add(x)
        if y != 'start':
            neighbors[x].add(y)
    return neighbors

def cave_generator(puzzle_input, part_2):
    queue = deque()
    start_path = (['start'], 'start', set(), None)
    queue.append(start_path)
    neighbors = get_neighbors(puzzle_input)

    while queue:
        path, most_recent, small_caves_visited, small_cave_visited_twice = queue.popleft()

        for neighbor in neighbors[most_recent]:
            new_path = path + [neighbor]
            if is_end(neighbor):
                yield new_path
            elif is_small(neighbor):
                new_small_caves_visited = small_caves_visited.union({neighbor})
                if part_2:
                    if small_cave_visited_twice is None:
                        new_small_cave_visited_twice = neighbor if neighbor in small_caves_visited else None
                        queue.append((new_path, neighbor, new_small_caves_visited, new_small_cave_visited_twice))
                    elif neighbor != small_cave_visited_twice and neighbor not in small_caves_visited:
                        queue.append((new_path, neighbor, new_small_caves_visited, small_cave_visited_twice))
                elif neighbor not in small_caves_visited:
                    queue.append((new_path, neighbor, new_small_caves_visited, None))
            else:
                queue.append((new_path, neighbor, small_caves_visited, small_cave_visited_twice))

def part_1(puzzle_input):
    return len(list(cave_generator(puzzle_input, False)))

def part_2(puzzle_input):
    return len(list(cave_generator(puzzle_input, True)))
