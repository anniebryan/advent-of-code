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


def get_squared_dists(coordinates: list[tuple[int, int, int]]) -> dict[tuple[int, int], float]:
    # (i, j) -> squared distance between coordinates[i] and coordinates[j]
    sq_dists = {}
    for i, (x1, y1, z1) in enumerate(coordinates):
        for j, (x2, y2, z2) in enumerate(coordinates):
            if i >= j:
                continue
            sq_dists[i, j] = (x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2
    return sq_dists


# TODO: speedup (currently ~10s)
def solve_part_1(puzzle_input: list[str]):
    num_connections, coordinates = parse_input(puzzle_input, False)
    dists = get_squared_dists(coordinates)

    connections = []
    for _ in range(num_connections):
        min_dist = min(dists.values())
        for (i, j), d in dists.items():
            x, y = coordinates[i], coordinates[j]
            if d == min_dist:
                connections.append((x, y))
                del dists[i, j]
                break

    g = nx.Graph()
    g.add_edges_from(connections)
    circuits = list(nx.connected_components(g))
    largest_3_circuits = sorted([len(c) for c in circuits], reverse=True)[:3]

    return prod(largest_3_circuits)


# TODO: speedup (currently ~80s)
def solve_part_2(puzzle_input: list[str]):
    _, coordinates = parse_input(puzzle_input, True)
    dists = get_squared_dists(coordinates)

    g = nx.Graph()
    g.add_nodes_from(coordinates)
    circuits = list(nx.connected_components(g))
    while len(circuits) > 1:
        min_dist = min(dists.values())
        for (i, j), d in dists.items():
            x, y = coordinates[i], coordinates[j]
            if d == min_dist:
                g.add_edge(x, y)
                del dists[i, j]
                break
        circuits = list(nx.connected_components(g))

    return x[0] * y[0]
