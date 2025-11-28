"""
Advent of Code 2024
Day 10: Hoof It
"""

from utils import DirectedGraph


def parse_input(puzzle_input: list[str]):
    loc_to_val = {}
    for i, row in enumerate(puzzle_input):
        for j, val in enumerate(row):
            loc_to_val[(i, j)] = val

    g = DirectedGraph()
    for i, row in enumerate(puzzle_input):
        for j, val in enumerate(row):
            if val != ".":
                for (di, dj) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                    neighbor = (i + di, j + dj)
                    if neighbor in loc_to_val and loc_to_val[neighbor] != "." and int(loc_to_val[neighbor]) == int(val) + 1:
                        g.insert_edge((i, j), neighbor)                    
    return g, loc_to_val


def path_exists(g: DirectedGraph, start: tuple[int, int], end: tuple[int, int], memo) -> bool:
    if (start, end) in memo:
        return memo[(start, end)]

    if start == end:
        memo[(start, end)] = True
        return True

    for n in g.graph[start]:
        if path_exists(g, n, end, memo):
            memo[(start, end)] = True
            return True

    memo[(start, end)] = False
    return False


def num_paths(g: DirectedGraph, start: tuple[int, int], end: tuple[int, int], memo) -> int:
    if (start, end) in memo:
        return memo[(start, end)]

    if start == end:
        memo[(start, end)] = 1
        return 1

    ans = sum([num_paths(g, n, end, memo) for n in g.graph[start]])
    memo[(start, end)] = ans
    return ans


def get_start_end_locs(loc_to_val):
    start_locs = {loc for loc, val in loc_to_val.items() if val == "0"}
    end_locs = {loc for loc, val in loc_to_val.items() if val == "9"}
    return start_locs, end_locs


def solve_part_1(puzzle_input: list[str]):
    g, loc_to_val = parse_input(puzzle_input)
    start_locs, end_locs = get_start_end_locs(loc_to_val)
    total_score = 0
    for start in start_locs:
        for end in end_locs:
            if path_exists(g, start, end, {}):
                total_score += 1
    return total_score


def solve_part_2(puzzle_input: list[str]):
    g, loc_to_val = parse_input(puzzle_input)
    start_locs, end_locs = get_start_end_locs(loc_to_val)
    total_rating = 0
    for start in start_locs:
        for end in end_locs:
            total_rating += num_paths(g, start, end, {})
    return total_rating
