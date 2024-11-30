"""
Advent of Code 2022
Day 18: Boiling Boulders
"""

from collections import defaultdict, deque


def get_sides(cube):
    x, y, z = cube
    return {
        ('xy', x - 1, y - 1, z - 1),
        ('xz', x - 1, y - 1, z - 1),
        ('yz', x - 1, y - 1, z - 1),
        ('xy', x - 1, y - 1, z),
        ('xz', x - 1, y, z - 1),
        ('yz', x, y - 1, z - 1)
    }

def get_all_sides(cubes):
    all_sides = defaultdict(int)
    for cube in cubes:
        for side in get_sides(cube):
            all_sides[side] += 1
    return all_sides


def unique_sides(cubes):
    all_sides = get_all_sides(cubes)
    return [s for s in all_sides if all_sides[s] == 1]


def neighbors(cube):
    x, y, z = cube
    yield (x + 1, y, z)
    yield (x - 1, y, z)
    yield (x, y + 1, z)
    yield (x, y - 1, z)
    yield (x, y, z + 1)
    yield (x, y, z - 1)


def unreachable_air_space(cubes):
    # maps (x, y, z) -> True if reachable, else False
    air_space = {}
    xs = list(map(lambda cube: cube[0], cubes))
    ys = list(map(lambda cube: cube[1], cubes))
    zs = list(map(lambda cube: cube[2], cubes))
    for x in range(min(xs) - 1, max(xs) + 1):
        for y in range(min(ys) - 1, max(ys) + 1):
            for z in range(min(zs) - 1, max(zs) + 1):
                if (x, y, z) not in cubes:
                    air_space[(x, y, z)] = False

    # run BFS
    queue = deque()
    seen = set()
    start = (min(xs) - 1, min(ys) - 1, min(zs) - 1)
    queue.append(start)
    seen.add(start)
    while queue:
        cube = queue.popleft()
        air_space[cube] = True
        for neighbor in neighbors(cube):
            if neighbor in air_space and neighbor not in seen:
                queue.append(neighbor)
                seen.add(neighbor)
    
    return [cube for cube in air_space if not air_space[cube]]


def part_1(puzzle_input):
    cubes = [tuple(int(x) for x in row.split(",")) for row in puzzle_input]
    return len(unique_sides(cubes))

def part_2(puzzle_input):
    cubes = [tuple(int(x) for x in row.split(",")) for row in puzzle_input]
    internal = set().union(side for cube in unreachable_air_space(cubes) for side in get_sides(cube))
    return len([side for side in unique_sides(cubes) if side not in internal])
