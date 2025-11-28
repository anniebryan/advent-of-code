"""
Advent of Code 2024
Day 12: Garden Groups
"""

import os
from collections import defaultdict, deque
from collections.abc import Iterator
from pathlib import Path

import click

from utils import Grid


def fill_region(g: Grid, i: int, j: int) -> set[tuple[int, int]]:
    # BFS
    region = {(i, j)}
    q = deque([(i, j)])
    while q:
        (ci, cj) = q.popleft()
        for (di, dj) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            x, y = ci + di, cj + dj
            if (x, y) not in region and g.in_bounds(x, y) and g.at(x, y) == g.at(ci, cj):
                region.add((x, y))
                q.append((x, y))
    return region


def get_all_regions(puzzle_input: list[str]) -> Iterator[tuple[int, int]]:
    g = Grid(puzzle_input)
    all_seen = set()
    for (i, j) in g:
        if (i, j) in all_seen:
            continue
        region = fill_region(g, i, j)
        yield region
        all_seen |= region


UndirectedEdge = tuple[tuple[int, int], tuple[int, int]]

def get_all_perimeter_edges(region: set[tuple[int, int]]) -> Iterator[UndirectedEdge]:
    for (i, j) in region:
        for (di, dj) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            if (i + di, j + dj) not in region:
                # exposed edge
                si, sj = i + max(di, 0), j + max(dj, 0)
                ei, ej = si + int(di == 0), sj + int(dj == 0)
                yield ((si, sj), (ei, ej))


def calc_perimeter(region: set[tuple[int, int]]) -> int:
    perim = 0
    for _ in get_all_perimeter_edges(region):
        perim += 1
    return perim


def get_dir(curr, prev) -> str:
    """Return "UD" for up and down, "LR" for left and right"""
    if prev is None:
        return None
    (ci, cj) = curr
    (pi, pj) = prev
    if ci == pi:
        return "LR"
    if cj == pj:
        return "UD"
    raise ValueError(f"Unexpected {curr=} {prev=}")


def calc_num_sides(region: set[tuple[int, int]]) -> int:
    # equivalent to counting the number of corners
    num_corners = 0
    vertex_to_edges = defaultdict(set)
    for (start, end) in get_all_perimeter_edges(region):
        vertex_to_edges[start].add(end)
        vertex_to_edges[end].add(start)
    for s in vertex_to_edges.values():
        if len(s) == 2:
            (e1i, e1j), (e2i, e2j) = s
            if e1i != e2i and e1j != e2j:
                num_corners += 1
        elif len(s) == 4:
            num_corners += 2
    return num_corners


def solve_part_1(puzzle_input: list[str]):
    tot = 0
    for region in get_all_regions(puzzle_input):
        area = len(region)
        perimeter = calc_perimeter(region)
        tot += area * perimeter
    return tot


def solve_part_2(puzzle_input: list[str]):
    tot = 0
    for region in get_all_regions(puzzle_input):
        area = len(region)
        num_sides = calc_num_sides(region)
        tot += area * num_sides
    return tot
