"""
Advent of Code 2024
Day 13: Claw Contraption
"""

import regex as re

COST = {"A": 3, "B": 1}
MAX_PRESSES = 100
PRIZE_OFFSET = 10000000000000


def parse_input(puzzle_input: list[str]):
    for i in range(0, len(puzzle_input), 4):
        a_match = re.match(r"X\+(?P<x>\d+), Y\+(?P<y>\d+)", puzzle_input[i].split(": ")[1])
        b_match = re.match(r"X\+(?P<x>\d+), Y\+(?P<y>\d+)", puzzle_input[i + 1].split(": ")[1])
        prize_match = re.match(r"X=(?P<x>\d+), Y=(?P<y>\d+)", puzzle_input[i + 2].split(": ")[1])

        a = (int(a_match.group('x')), int(a_match.group('y')))
        b = (int(b_match.group('x')), int(b_match.group('y')))
        prize = (int(prize_match.group('x')), int(prize_match.group('y')))

        yield (a, b, prize)


def get_num_tokens(a: tuple[int, int], b: tuple[int, int], prize: tuple[int, int], part_2: bool) -> int:
    """If it is not possible to win, returns 0."""
    a_x, a_y = a
    b_x, b_y = b
    p_x, p_y = prize

    if part_2:
        p_x += PRIZE_OFFSET
        p_y += PRIZE_OFFSET

    # solve 2x2 system of equations
    matrix_det = a_x * b_y - a_y * b_x
    n_a = (b_y * p_x - b_x * p_y)
    n_b = (a_x * p_y - a_y * p_x)

    # only return if solution is an integer
    if n_a % matrix_det == 0 and n_b % matrix_det == 0:
        if part_2 or (int(n_a / matrix_det) <= MAX_PRESSES and int(n_b / matrix_det) <= MAX_PRESSES):
            return int(n_a / matrix_det) * COST["A"] + int(n_b / matrix_det) * COST["B"]

    return 0


def solve_part_1(puzzle_input: list[str]):
    return sum(get_num_tokens(a, b, prize, False) for (a, b, prize) in parse_input(puzzle_input))


def solve_part_2(puzzle_input: list[str]):
    return sum(get_num_tokens(a, b, prize, True) for (a, b, prize) in parse_input(puzzle_input))
