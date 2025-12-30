"""
Advent of Code 2023
Day 24: Never Tell Me The Odds
"""

import re

import numpy as np


def parse_input(puzzle_input: list[str], part_2: bool):
    match = re.match(r"test area: (?P<min_area>\d+)\-(?P<max_area>\d+)", puzzle_input[0])
    assert match is not None
    min_bounds = int(match.group("min_area"))
    max_bounds = int(match.group("max_area"))

    stones = []
    for line in puzzle_input[1:]:
        pos, vel = line.split(" @ ")
        px, py, pz = map(int, pos.split(", "))
        vx, vy, vz = map(int, vel.split(", "))
        stones.append((px, py, pz, vx, vy, vz))
    return min_bounds, max_bounds, stones


def solve_part_1(puzzle_input: list[str]):
    min_bounds, max_bounds, stones = parse_input(puzzle_input, False)

    num_intersections_in_test_area = 0
    for i, (px1, py1, _, vx1, vy1, _) in enumerate(stones):
        for (px2, py2, _, vx2, vy2, _) in stones[i + 1:]:
            m1, m2 = (vy1 / vx1), (vy2 / vx2)
            if m1 == m2:
                continue
            x = (py2 - py1 + m1 * px1 - m2 * px2) / (m1 - m2)
            y = py1 + m1 * (x - px1)
            t1 = (x - px1) / vx1
            t2 = (x - px2) / vx2
            if (t1 >= 0) and (t2 >= 0) and (min_bounds <= x <= max_bounds) and (min_bounds <= y <= max_bounds):
                num_intersections_in_test_area += 1

    return num_intersections_in_test_area


def solve_part_2(puzzle_input: list[str]):
    _, _, stones = parse_input(puzzle_input, True)

    # we only need 4 stones' positions/velocities to solve for 6 unknowns
    # since each pair of stones gives us 2 equations
    (
        (x1, y1, z1, vx1, vy1, vz1),
        (x2, y2, z2, vx2, vy2, vz2),
        (x3, y3, z3, vx3, vy3, vz3),
        (x4, y4, z4, vx4, vy4, vz4),
    ) = stones[:4]

    # README.md contains derivation of matrix A and vector b
    A = np.array([
        [vy2 - vy1, -(vx2 - vx1), 0, -(y2 - y1), x2 - x1, 0],
        [vz2 - vz1, 0, -(vx2 - vx1), -(z2 - z1), 0, x2 - x1],
        [vy3 - vy2, -(vx3 - vx2), 0, -(y3 - y2), x3 - x2, 0],
        [vz3 - vz2, 0, -(vx3 - vx2), -(z3 - z2), 0, x3 - x2],
        [vy4 - vy3, -(vx4 - vx3), 0, -(y4 - y3), x4 - x3, 0],
        [vz4 - vz3, 0, -(vx4 - vx3), -(z4 - z3), 0, x4 - x3],
    ])
    b = np.array([
        -x1 * vy1 + x2 * vy2 + y1 * vx1 - y2 * vx2,
        -x1 * vz1 + x2 * vz2 + z1 * vx1 - z2 * vx2,
        -x2 * vy2 + x3 * vy3 + y2 * vx2 - y3 * vx3,
        -x2 * vz2 + x3 * vz3 + z2 * vx2 - z3 * vx3,
        -x3 * vy3 + x4 * vy4 + y3 * vx3 - y4 * vx4,
        -x3 * vz3 + x4 * vz4 + z3 * vx3 - z4 * vx4,
    ])
    [x, y, z, _, _, _] = map(round, np.linalg.solve(A, b))

    return int(x + y + z)
