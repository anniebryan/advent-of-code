"""
Advent of Code 2024
Day 6: Guard Gallivant
"""

def parse_input(puzzle_input: list[str]):
    obstacle_locations = set()
    guard_loc = None
    for i, row in enumerate(puzzle_input):
        for j, val in enumerate(row):
            if val == "#":
                obstacle_locations.add((i, j))
            elif val == "^":
                guard_loc = (i, j)
    puzzle_size = (len(puzzle_input), len(puzzle_input[0]))
    return obstacle_locations, guard_loc, puzzle_size


def guard_in_map_bounds(guard_loc, puzzle_size):
    i, j = guard_loc
    height, width = puzzle_size
    return 0 <= i < height and 0 <= j < width


def move(guard_loc, direction):
    return (guard_loc[0] + direction[0], guard_loc[1] + direction[1])


def rotate_90deg_right(direction):
    return {(-1, 0): (0, 1), (0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0)}[direction]


def caught_in_loop(puzzle_size, obstacle_locations, guard_loc):
    direction = (-1, 0)
    seen = {(guard_loc, direction)}
    while True:
        next_loc = move(guard_loc, direction)
        while next_loc not in obstacle_locations:
            if not guard_in_map_bounds(next_loc, puzzle_size):
                return False
            if (next_loc, direction) in seen:
                return True
            seen.add((next_loc, direction))
            guard_loc = next_loc
            next_loc = move(guard_loc, direction)
        direction = rotate_90deg_right(direction)


def get_all_guard_locs(obstacle_locations, guard_loc, puzzle_size):
    direction = (-1, 0)
    all_guard_locs = {guard_loc}
    while True:
        next_loc = move(guard_loc, direction)
        while next_loc not in obstacle_locations:
            if not guard_in_map_bounds(next_loc, puzzle_size):
                return all_guard_locs
            all_guard_locs.add(next_loc)
            guard_loc = next_loc
            next_loc = move(guard_loc, direction)
        direction = rotate_90deg_right(direction)


def solve_part_1(puzzle_input: list[str]):
    obstacle_locations, guard_loc, puzzle_size = parse_input(puzzle_input)
    return len(get_all_guard_locs(obstacle_locations, guard_loc, puzzle_size))


def solve_part_2(puzzle_input: list[str]):
    obstacle_locations, guard_loc, puzzle_size = parse_input(puzzle_input)
    candidates = get_all_guard_locs(obstacle_locations, guard_loc, puzzle_size) - {guard_loc}
    num_pos = 0
    for cand in candidates:
        if caught_in_loop(puzzle_size, obstacle_locations | {cand}, guard_loc):
            num_pos += 1
    return num_pos
