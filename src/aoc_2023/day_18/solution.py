"""
Advent of Code 2023
Day 18: Lavaduct Lagoon
"""

import re
from collections import defaultdict


def parse_input(
        puzzle_input: list[str],
        part_2: bool,
) -> tuple[dict[int, list[tuple[int, int]]], dict[int, list[tuple[int, int]]]]:

    horizontal_edges = defaultdict(list)
    vertical_edges = defaultdict(list)
    curr_x, curr_y = 0, 0

    for line in puzzle_input:
        if part_2:
            match = re.match(r"[UDLR] \d+ \(#(?P<hex>.*)\)", line)
            assert match is not None
            hex = match.group("hex")
            direction = "RDLU"[int(hex[-1])]
            num_steps = int(hex[:-1], 16)
        else:
            direction = line[0]
            num_steps = int(line.split()[1])

        match direction:
            case "R":
                horizontal_edges[curr_y].append((curr_x, curr_x + num_steps))
                curr_x += num_steps
            case "D":
                vertical_edges[curr_x].append((curr_y, curr_y + num_steps))
                curr_y += num_steps
            case "L":
                horizontal_edges[curr_y].append((curr_x - num_steps, curr_x))
                curr_x -= num_steps
            case "U":
                vertical_edges[curr_x].append((curr_y - num_steps, curr_y))
                curr_y -= num_steps

    return horizontal_edges, vertical_edges


def _solve(puzzle_input: list[str], part_2: bool) -> int:
    horizontal_edges, vertical_edges = parse_input(puzzle_input, part_2)

    ys = sorted(horizontal_edges.keys())
    xs = sorted(vertical_edges.keys())

    interior_area = 0
    prev_row = []

    for j, (y_prev, y_curr) in enumerate(zip(ys, ys[1:])):
        curr_row = []

        for i, (x_prev, x_curr) in enumerate(zip(xs, xs[1:])):
            # check if there is a vertical boundary on the left of this cell
            has_vert_edge_on_left = any(y0 <= y_prev and y_curr <= y1 for y0, y1 in vertical_edges.get(x_prev, []))

            left_cell_is_inside = i > 0 and curr_row[i - 1]
            above_cell_is_inside = j > 0 and prev_row[i]

            if left_cell_is_inside != has_vert_edge_on_left:
                curr_row.append(True)
                cell_height = y_curr - y_prev - 1
                cell_width = x_curr - x_prev - 1
                interior_area += cell_height * cell_width

                if left_cell_is_inside:
                    interior_area += cell_height
                if above_cell_is_inside:
                    interior_area += cell_width
                if left_cell_is_inside and not has_vert_edge_on_left and above_cell_is_inside and prev_row[i - 1]:
                    interior_area += 1
            else:
                curr_row.append(False)
        prev_row = curr_row

    vertical_boundary = sum(y1 - y0 + 1 for segments in vertical_edges.values() for y0, y1 in segments)
    horizontal_boundary = sum(x1 - x0 + 1 for segments in horizontal_edges.values() for x0, x1 in segments)
    # avoid double counting
    num_corners = sum(len(v) for v in vertical_edges.values()) + sum(len(h) for h in horizontal_edges.values())

    return interior_area + vertical_boundary + horizontal_boundary - num_corners


def solve_part_1(puzzle_input: list[str]):
    return _solve(puzzle_input, part_2=False)


def solve_part_2(puzzle_input: list[str]):
    return _solve(puzzle_input, part_2=True)
