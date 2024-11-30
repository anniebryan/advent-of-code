"""
Advent of Code 2021
Day 11: Dumbo Octopus
"""

from collections import deque


def get_octopus_dict(puzzle_input):
    octopuses = [[int(val) for val in str(int(row))] for row in puzzle_input]
    num_rows, num_cols = len(octopuses), len(octopuses[0])
    num_octopuses = num_rows * num_cols
    octopus_dict = {(i, j): octopuses[j][i] for i in range(num_cols) for j in range(num_rows)}
    return octopus_dict, num_rows, num_cols, num_octopuses


def get_neighbors(num_rows, num_cols, i, j):
    locs = set()
    if i != 0:
        locs.add((i - 1, j))  # left
        if j != 0:
            locs.add((i - 1, j - 1))  # top left
        if j != num_rows - 1:
            locs.add((i - 1, j + 1))  # bottom left

    if i != num_cols - 1:
        locs.add((i + 1, j))  # right
        if j != 0:
            locs.add((i + 1, j - 1))  # top right
        if j != num_rows - 1:
            locs.add((i + 1, j + 1))  # bottom right

    if j != 0:
        locs.add((i, j - 1))  # up
    if j != num_rows - 1:
        locs.add((i, j + 1))  # down

    return locs


def timestep(num_rows, num_cols, d):
    new_d = d
    flashed = set()
    queue = deque()
    for loc in d:
        if d[loc] == 9:
            flashed.add(loc)
            for neighbor in get_neighbors(num_rows, num_cols, *loc):
                queue.append(neighbor)
        else:
            new_d[loc] = new_d[loc] + 1

    while queue:
        loc = queue.popleft()
        if loc not in flashed:
            if new_d[loc] == 9:
                flashed.add(loc)
                for neighbor in get_neighbors(num_rows, num_cols, *loc):
                    queue.append(neighbor)
            else:
                new_d[loc] = new_d[loc] + 1
    
    for loc in flashed:
        new_d[loc] = 0

    return new_d, len(flashed)


def n_timesteps(octopus_dict, num_rows, num_cols, n):
    total_flashed = 0
    for _ in range(n):
        octopus_dict, num_flashed = timestep(num_rows, num_cols, octopus_dict)
        total_flashed += num_flashed
    return total_flashed


def run_until_all_flashed(octopus_dict, num_rows, num_cols, num_octopuses):
    i = 0
    while True:
        i += 1
        octopus_dict, num_flashed = timestep(num_rows, num_cols, octopus_dict)
        if num_flashed == num_octopuses:
            return i


def part_1(puzzle_input):
    octopus_dict, num_rows, num_cols, _ = get_octopus_dict(puzzle_input)
    return n_timesteps(octopus_dict, num_rows, num_cols, 100)


def part_2(puzzle_input):
    octopus_dict, num_rows, num_cols, num_octopuses = get_octopus_dict(puzzle_input)
    return run_until_all_flashed(octopus_dict, num_rows, num_cols, num_octopuses)
