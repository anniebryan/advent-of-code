"""
Advent of Code 2024
Day 16: Reindeer Maze
"""

from collections import defaultdict, deque

from utils import Grid


def all_possible_scores(grid: Grid) -> set[int]:
    start = grid.where("S")[0]

    min_scores = {}
    final_scores = set()
    all_locs_in_paths = defaultdict(set)
    q = deque([(start, (0, 1), 0, [start])])

    while q:
        curr, direction, score, path = q.popleft()
        if (curr, direction) in min_scores and score > min_scores[(curr, direction)]:
            continue

        min_scores[(curr, direction)] = score
        i, j = curr
        di, dj = direction
        ni, nj = i + di, j + dj

        if grid.at(ni, nj) == "E":
            final_scores.add(score + 1)
            for loc in path + [(ni, nj)]:
                all_locs_in_paths[score + 1].add(loc)
            continue

        if grid.at(ni, nj) != "#":
            q.append(((ni, nj), direction, score + 1, path + [(ni, nj)]))

        q.append((curr, (-dj, di), score + 1000, path))
        q.append((curr, (dj, -di), score + 1000, path))

    return final_scores, all_locs_in_paths


def solve_part_1(puzzle_input: list[str]):
    grid = Grid(puzzle_input)
    final_scores, _ = all_possible_scores(grid)
    return min(final_scores)


def solve_part_2(puzzle_input: list[str]):
    grid = Grid(puzzle_input)
    final_scores, all_locs_in_paths = all_possible_scores(grid)
    return len(all_locs_in_paths[min(final_scores)])
