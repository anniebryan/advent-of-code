"""
Advent of Code 2017
Day 11: Hex Ed
"""


def parse_input(puzzle_input: list[str], part_2: bool):
    return puzzle_input[0].split(",")


def _take_step(i: int, j: int, step: str) -> tuple[int, int]:
    return {
        "n": (i, j + 2),
        "ne": (i + 1, j + 1),
        "se": (i + 1, j - 1),
        "s": (i, j - 2),
        "sw": (i - 1, j - 1),
        "nw": (i - 1, j + 1),
    }[step]


def _hex_distance(i: int, j: int) -> int:
    q = i
    r = (j - i) // 2
    return max(abs(q), abs(r), abs(q + r))


def solve_part_1(puzzle_input: list[str]):
    steps = parse_input(puzzle_input, False)

    i, j = 0, 0
    for step in steps:
        i, j = _take_step(i, j, step)

    return _hex_distance(i, j)


def solve_part_2(puzzle_input: list[str]):
    steps = parse_input(puzzle_input, True)

    i, j = 0, 0
    max_dist = _hex_distance(i, j)
    for step in steps:
        i, j = _take_step(i, j, step)
        max_dist = max(max_dist, _hex_distance(i, j))

    return max_dist
