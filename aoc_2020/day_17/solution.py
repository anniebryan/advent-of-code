"""
Advent of Code 2020
Day 17: Conway Cubes
"""

def initial_active(puzzle_input, num_dim):
    active = set()
    for i in range(len(puzzle_input)):
        row = puzzle_input[i]
        for j in range(len(row)):
            if row[j] == '#':
                if num_dim == 3:
                    active.add((i, j, 0))
                else:
                    active.add((i, j, 0, 0))
    return active


def neighbors(cube, num_dim):
    x, y, z = cube[:3]
    if num_dim == 4:
        w = cube[3]
    ns = set()
    for i in {x - 1, x, x + 1}:
        for j in {y - 1, y, y + 1}:
            for k in {z - 1, z, z + 1}:
                if num_dim == 4:
                    for l in {w - 1, w, w + 1}:
                        if x != i or y != j or z != k or w != l:
                            ns.add((i, j, k, l))
                else:
                    if x != i or y != j or z != k:
                        ns.add((i, j, k))
    return ns


def num_active(neighbors, active):
    return len(list(filter(lambda x: x in active, neighbors)))


def add_cube(cube, active, num_dim):
    if cube in active:
        return num_active(neighbors(cube, num_dim), active) in {2, 3}
    else:
        return num_active(neighbors(cube, num_dim), active) == 3


def run_cycle(active, num_dim):
    min_x, max_x = min(active, key=lambda x:x[0])[0], max(active, key=lambda x:x[0])[0]
    min_y, max_y = min(active, key=lambda x:x[1])[1], max(active, key=lambda x:x[1])[1]
    min_z, max_z = min(active, key=lambda x:x[2])[2], max(active, key=lambda x:x[2])[2]
    if num_dim == 4:
        min_w, max_w = min(active, key=lambda x:x[3])[3], max(active, key=lambda x:x[3])[3]
    new_active = set()
    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            for z in range(min_z - 1, max_z + 2):
                if num_dim == 3:
                    cube = (x, y, z)
                    if add_cube(cube, active, num_dim):
                            new_active.add(cube)
                else:
                    for w in range(min_w - 1, max_w + 2):
                        cube = (x, y, z, w)
                        if add_cube(cube, active, num_dim):
                            new_active.add(cube)
                    
    return new_active


def run_n_cycles(puzzle_input, n, num_dim):
    active = initial_active(puzzle_input, num_dim)
    for _ in range(n):
        active = run_cycle(active, num_dim)
    return active


def solve_part_1(puzzle_input):
    return len(run_n_cycles(puzzle_input, 6, 3))


def solve_part_2(puzzle_input):
    return len(run_n_cycles(puzzle_input, 6, 4))
