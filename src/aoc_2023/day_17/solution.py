"""
Advent of Code 2023
Day 17: Clumsy Crucible
"""

import heapq

from aoc_utils import DirectedWeightedGraph


def parse_input(puzzle_input: list[str], part_2: bool) -> DirectedWeightedGraph:
    g = DirectedWeightedGraph()
    for i, line in enumerate(puzzle_input):
        for j, val in enumerate(line):
            if j > 0:
                g.insert_edge((i, j - 1), (i, j), int(val))
            if j < len(line) - 1:
                g.insert_edge((i, j + 1), (i, j), int(val))
            if i > 0:
                g.insert_edge((i - 1, j), (i, j), int(val))
            if i < len(puzzle_input) - 1:
                g.insert_edge((i + 1, j), (i, j), int(val))
    return g


def get_min_path_cost(
        puzzle_input: list[str],
        min_steps_before_turn: int | None,
        max_steps_before_turn: int | None,
) -> int:
    g = parse_input(puzzle_input, False)
    
    start = (0, 0)
    target = (len(puzzle_input) - 1, len(puzzle_input[0]) - 1)

    q = []  # (distance, node, current direction, # of steps in current direction, path)
    dists = {}  # (node, direction, # of steps) -> distance
    paths = {}  # (node, direction, # of steps) -> path
    visited = set()  # (node, direction, # of steps)

    for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        q.append((0, start, dir, 0, []))
        dists[(start, dir, 0)] = 0

    while q:
        dist_so_far, curr, curr_dir, num_steps, path = heapq.heappop(q)
        if (curr, curr_dir, num_steps) not in visited:
            visited.add((curr, curr_dir, num_steps))
            for n in g.neighbors[curr]:
                new_dir = (n[0] - curr[0], n[1] - curr[1])

                if min_steps_before_turn is not None and new_dir != curr_dir and num_steps < min_steps_before_turn:
                    continue  # must continue in the same direction for at least `min_steps_before_turn` steps
                if max_steps_before_turn is not None and new_dir == curr_dir and num_steps >= max_steps_before_turn:
                    continue  # cannot move more than `max_steps_before_turn` steps in one direction
                if (new_dir[0] * -1, new_dir[1] * -1) == curr_dir:
                    continue  # cannot go back in the direction we came from

                w = g.weights[(curr, n)]
                new_dist = dist_so_far + w
                new_num_steps = num_steps + 1 if new_dir == curr_dir else 1
                new_key = (n, new_dir, new_num_steps)
                if new_key not in dists or dists[new_key] > new_dist:
                    dists[new_key] = new_dist
                    paths[new_key] = path + [n]
                    heapq.heappush(q, (new_dist, n, new_dir, new_num_steps, path + [n]))
    if min_steps_before_turn is None:
        candidate_dists = [dists[k] for k in dists.keys() if k[0] == target]
    else:
        candidate_dists = [dists[k] for k in dists.keys() if k[0] == target and k[2] >= min_steps_before_turn]
    return min(candidate_dists)


def solve_part_1(puzzle_input: list[str]):
    return get_min_path_cost(puzzle_input, None, 3)

def solve_part_2(puzzle_input: list[str]):
    return get_min_path_cost(puzzle_input, 4, 10)
