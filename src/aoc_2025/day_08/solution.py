"""
Advent of Code 2025
Day 8: Playground
"""

from math import prod

import networkx as nx


def parse_input(puzzle_input: list[str], part_2: bool):
    num_connections = int(puzzle_input[0])
    coordinates = []
    for line in puzzle_input[1:]:
        c = line.split(",")
        x, y, z = int(c[0]), int(c[1]), int(c[2])
        coordinates.append((x, y, z))
    return num_connections, coordinates


def get_dists(coordinates: list[tuple[int, int, int]]) -> dict[int, tuple]:
    # (i, j) -> squared distance between coordinates[i] and coordinates[j]
    sq_dists = {}
    for i, (x1, y1, z1) in enumerate(coordinates):
        for j, (x2, y2, z2) in enumerate(coordinates):
            if i >= j:
                continue
            sq_dists[i, j] = (x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2

    sq_dist_to_pair = {}
    for (i, j), d in sq_dists.items():
        if d in sq_dist_to_pair:
            raise ValueError(f"Multiple pairs of coordinates have the same distance {d}")
        sq_dist_to_pair[d] = (coordinates[i], coordinates[j])
    return sq_dist_to_pair


def solve_part_1(puzzle_input: list[str]):
    num_connections, coordinates = parse_input(puzzle_input, False)
    dists = get_dists(coordinates)

    g = nx.Graph()
    g.add_nodes_from(coordinates)

    for i, (_, (x, y)) in enumerate(sorted(dists.items())):
        g.add_edge(x, y)
        if i == num_connections:
            break

    return prod(sorted([len(c) for c in nx.connected_components(g)], reverse=True)[:3])


def solve_part_2(puzzle_input: list[str]):
    _, coordinates = parse_input(puzzle_input, True)
    dists = get_dists(coordinates)

    g = nx.Graph()
    g.add_nodes_from(coordinates)

    for _, (x, y) in sorted(dists.items()):
        g.add_edge(x, y)
        if nx.number_connected_components(g) == 1:
            break

    return x[0] * y[0]
