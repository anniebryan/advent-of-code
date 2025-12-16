"""
Advent of Code 2025
Day 9: Movie Theater
"""

def parse_input(puzzle_input: list[str], part_2: bool):
    locs = []
    for line in puzzle_input:
        x, y = line.split(",")
        locs.append((int(x), int(y)))
    return locs


def any_edges_intersect(
        x1: int, y1: int,
        x2: int, y2: int,
        edges: set[tuple[int, int, int, int]],
) -> bool:
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    for (e_x1, e_y1, e_x2, e_y2) in edges:
        min_ex, max_ex = min(e_x1, e_x2), max(e_x1, e_x2)
        min_ey, max_ey = min(e_y1, e_y2), max(e_y1, e_y2)
        if (min_x < max_ex) and (max_x > min_ex) and (min_y < max_ey) and (max_y > min_ey):
            return True
    return False


def solve_part_1(puzzle_input: list[str]):
    locs = parse_input(puzzle_input, False)
    max_rect_size = 0
    for (x1, y1) in locs:
        for (x2, y2) in locs:
            rect_size = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            max_rect_size = max(max_rect_size, rect_size)
    return max_rect_size


def solve_part_2(puzzle_input: list[str]):
    locs = parse_input(puzzle_input, True)

    edges = set()
    for (x1, y1), (x2, y2) in zip(locs, locs[1:] + [locs[0]]):
        edges.add((x1, y1, x2, y2))

    max_rect_size = 0
    for (x1, y1) in locs:
        for (x2, y2) in locs:
            rect_size = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            if rect_size > max_rect_size:
                if not any_edges_intersect(x1, y1, x2, y2, edges):
                    max_rect_size = max(max_rect_size, rect_size)
    return max_rect_size
