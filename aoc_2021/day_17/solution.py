"""
Advent of Code 2021
Day 17: Trick Shot
"""

def get_target_area(puzzle_input):
    return [[int(x) for x in puzzle_input[0].split(',')[i].split('=')[1].split('..')] for i in range(2)]


def x_in_range(x_pos, target_area):
    x_range = target_area[0]
    x_min, x_max = x_range
    if x_pos < x_min:
        return -1  # too far left
    if x_pos > x_max:
        return 1  # too far right
    return 0  # within the range


def y_in_range(y_pos, target_area):
    y_range = target_area[1]
    y_min, y_max = y_range
    if y_pos < y_min:
        return -1  # too high
    if y_pos > y_max:
        return 1  # too low
    return 0  # within the range


def in_target_area(x_pos, y_pos, target_area):
    return x_in_range(x_pos, target_area) == 0 and y_in_range(y_pos, target_area) == 0


def step(x_pos, y_pos, x_vel, y_vel):
    x_pos += x_vel
    y_pos += y_vel
    if x_vel > 0:
        x_vel -= 1
    elif x_vel < 0:
        x_vel += 1
    else:
        x_vel = 0
    y_vel -= 1
    return x_pos, y_pos, x_vel, y_vel


def hits_target_area(x_vel, y_vel, target_area):
    x_pos, y_pos = (0, 0)
    while not in_target_area(x_pos, y_pos, target_area):
        x_pos, y_pos, x_vel, y_vel = step(x_pos, y_pos, x_vel, y_vel)
        if y_in_range(y_pos, target_area) == -1:
            return False
        if x_in_range(x_pos, target_area) == 1:
            return False
    return True


def max_y_pos(x_vel, y_vel):
    x_pos, y_pos = (0, 0)
    max_y = y_pos
    while y_vel > 0:
        x_pos, y_pos, x_vel, y_vel = step(x_pos, y_pos, x_vel, y_vel)
        max_y = max(max_y, y_pos)
    return max_y


def max_y_pos_hits_target(target_area):
    max_y = 0
    best_x_vel, best_y_vel = None, None
    for x_vel in range(1, 241):
        for y_vel in range(1, 500):
            if hits_target_area(x_vel, y_vel, target_area):
                new_max = max_y_pos(x_vel, y_vel)
                if new_max > max_y:
                    max_y = new_max
                    best_x_vel, best_y_vel = x_vel, y_vel
    return max_y, best_x_vel, best_y_vel


def num_distinct_init_velocities(target_area):
    num_velocities = 0
    for x_vel in range(1, 241):
        for y_vel in range(-126, 500):
            if hits_target_area(x_vel, y_vel, target_area):
                num_velocities += 1
    return num_velocities


def solve_part_1(puzzle_input):
    target_area = get_target_area(puzzle_input)
    ans = max_y_pos_hits_target(target_area)
    return ans[0]


def solve_part_2(puzzle_input):
    target_area = get_target_area(puzzle_input)
    return num_distinct_init_velocities(target_area)
