"""
Advent of Code 2025
Day 4: Printing Department
"""

from aoc_utils import Grid


def parse_input(puzzle_input: list[str], part_2: bool) -> Grid:
    return Grid(puzzle_input)


def _get_accessible_rolls(g: Grid) -> set[tuple[int, int]]:
    accessible_rolls = set()
    for (x, y) in g:
        num_adj_rolls = 0
        if g.at(x, y) != "@":
            continue
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # (x, y) is not a neighbor of itself
                nx, ny = x + dx, y + dy
                if g.in_bounds(nx, ny) and g.at(nx, ny) == "@":
                    num_adj_rolls += 1
        if num_adj_rolls < 4:
            accessible_rolls.add((x, y))
    return accessible_rolls


def solve_part_1(puzzle_input: list[str]):
    g = parse_input(puzzle_input, False)
    return len(_get_accessible_rolls(g))


def solve_part_2(puzzle_input: list[str]):
    g = parse_input(puzzle_input, True)
    total_num_accessible = 0
    accessible_rolls = _get_accessible_rolls(g)
    while accessible_rolls:
        total_num_accessible += len(accessible_rolls)
        for (x, y) in accessible_rolls:
            g.set(x, y, ".")
        accessible_rolls = _get_accessible_rolls(g)
    return total_num_accessible
