"""
Advent of Code 2022
Day 22: Monkey Map
"""

import re

from aoc_utils import Cube, Grid


def parse_input(puzzle_input: list[str], part_2: bool):
    grid = Grid()
    for i, line in enumerate(puzzle_input):
        if line == "":
            break
        for j, char in enumerate(line):
            if char != " ":
                grid.set(i, j, char)
    path = []
    for ch in re.findall(r"(\d+|L|R)", puzzle_input[i + 1]):
        if ch in {"L", "R"}:
            path.append(ch)
        else:
            path.append(int(ch))
    return grid, path


def solve_part_1(puzzle_input: list[str]):
    grid, path = parse_input(puzzle_input, False)

    i, j = min({loc for loc, val in grid.values_at_row(0).items() if val == "."})
    di, dj = (0, 1)  # facing right

    for step in path:
        if step == "L":
            di, dj = -dj, di
        elif step == "R":
            di, dj = dj, -di
        else:
            for _ in range(step):
                ni, nj = i + di, j + dj
                if not grid.in_bounds(ni, nj):  # wrap around
                    if (di, dj) == (0, 1):  # facing right
                        nj = min({col for (_, col), val in grid.values_at_row(i).items() if val != " "})
                        assert grid.in_bounds(ni, nj)
                    elif (di, dj) == (0, -1):  # facing left
                        nj = max({col for (_, col), val in grid.values_at_row(i).items() if val != " "})
                        assert grid.in_bounds(ni, nj)
                    elif (di, dj) == (1, 0):  # facing down
                        ni = min({row for (row, _), val in grid.values_at_column(j).items() if val != " "})
                        assert grid.in_bounds(ni, nj)
                    elif (di, dj) == (-1, 0):  # facing up
                        ni = max({row for (row, _), val in grid.values_at_column(j).items() if val != " "})
                        assert grid.in_bounds(ni, nj)
                    else:
                        raise ValueError("Invalid direction")
                if grid.at(ni, nj) == "#":
                    break  # stop moving in this direction
                grid.set(ni, nj, {(0, 1): ">", (0, -1): "<", (1, 0): "v", (-1, 0): "^"}[(di, dj)])
                i, j = ni, nj

    facing = {(0, 1): 0, (1, 0): 1, (0, -1): 2, (-1, 0): 3}[(di, dj)]
    return 1000 * (i + 1) + 4 * (j + 1) + facing


def solve_part_2(puzzle_input: list[str]):
    grid, path = parse_input(puzzle_input, True)

    cube = Cube.from_grid(grid)

    start_col = min(
        col for (row, col), tile in grid.values.items() if row == 0 and tile == "."
    )
    face_id, row, col = cube.map_point(0, start_col)
    facing = 0  # facing right

    for step in path:
        if step == "L":
            facing = (facing - 1) % 4
        elif step == "R":
            facing = (facing + 1) % 4
        else:
            for _ in range(step):
                d_row, d_col = Cube.DIRS[facing]
                next_face = face_id
                next_row = row + d_row
                next_col = col + d_col
                next_facing = facing
                if not (0 <= next_row < cube.face_size and 0 <= next_col < cube.face_size):
                    next_face, next_row, next_col, next_facing = cube.cross_edge(
                        face_id, row, col, facing
                    )
                if cube.faces[next_face].at(next_row, next_col) == "#":
                    break
                face_id, row, col, facing = next_face, next_row, next_col, next_facing

    row, col = cube.unmap_point(face_id, row, col)
    return 1000 * (row + 1) + 4 * (col + 1) + facing
