"""
Advent of Code 2023
Day 23: A Long Walk
"""

import heapq
from collections import defaultdict

import numpy as np

from aoc_utils import Grid


def parse_input(puzzle_input: list[str], part_2: bool):
    grid = Grid.from_puzzle_input(puzzle_input)
    start = [i for i, ch in enumerate(puzzle_input[0]) if ch == "."][0]
    end = [i for i, ch in enumerate(puzzle_input[-1]) if ch == "."][0]

    grid.set(0, start, "S")
    grid.set(len(puzzle_input) - 1, end, "E")
    return grid


def solve_part_1(puzzle_input: list[str]):
    grid = parse_input(puzzle_input, False)
    start, end = grid.where("S")[0], grid.where("E")[0]

    # modified version of Grid.dijkstra
    q = [(0, [start])]
    dists = defaultdict(set)
    dists[start].add(0)

    while q:
        dist_so_far, path = heapq.heappop(q)
        curr = path[-1]
        dists[curr].add(dist_so_far)

        for n in grid.neighbors(curr):
            if (
                (grid.at(*curr) == ">" and n != (curr[0], curr[1] + 1))
                or (grid.at(*curr) == "<" and n != (curr[0], curr[1] - 1))
                or (grid.at(*curr) == "^" and n != (curr[0] - 1, curr[1]))
                or (grid.at(*curr) == "v" and n != (curr[0] + 1, curr[1]))
            ):
                continue
            if n not in path:
                heapq.heappush(q, (dist_so_far + 1, path + [n]))

    return max(dists[end])


def build_graph(grid: Grid) -> dict[tuple[int, int], dict[tuple[int, int], int]]:
    nodes = {
        (i, j) for (i, j) in grid
        if grid.at(i, j) != "#" and len(list(grid.neighbors((i, j)))) != 2
    }

    graph = {n: {} for n in nodes}

    for node in nodes:
        for neighbor in grid.neighbors(node):
            if neighbor in nodes:
                graph[node][neighbor] = 1
                continue

            prev = node
            curr = neighbor
            dist = 1

            while curr not in nodes:
                neighbors = list(grid.neighbors(curr))
                next_step = neighbors[0] if neighbors[1] == prev else neighbors[1]
                prev, curr = curr, next_step
                dist += 1

            graph[node][curr] = dist

    return graph


def max_path_length_dfs(
        graph: dict[tuple[int, int], dict[tuple[int, int], int]],
        node: tuple[int, int],
        end: tuple[int, int],
        visited: set[tuple[int, int]],
) -> float:
    if node == end:
        return 0

    best = -1 * np.inf
    for node, weight in graph[node].items():
        if node in visited:
            continue
        best = max(best, weight + max_path_length_dfs(graph, node, end, visited | {node}))

    return best


def solve_part_2(puzzle_input: list[str]):
    grid = parse_input(puzzle_input, True)
    start, end = grid.where("S")[0], grid.where("E")[0]

    graph = build_graph(grid)
    return max_path_length_dfs(graph, start, end, {start})
