"""
Advent of Code 2024
Day 21: Keypad Conundrum
"""

from collections import defaultdict

from utils import Grid

NUMERIC_KEYPAD = Grid(["789", "456", "123", ".0A"])
DIRECTIONAL_KEYPAD = Grid([".^A", "<v>"])


def shortest_path(start_key: str, dest_key: str, keypad: Grid) -> str:
    (start_i, start_j) = keypad.where(start_key)[0]
    (dest_i, dest_j) = keypad.where(dest_key)[0]

    vertical = "v" * (dest_i - start_i) if dest_i > start_i else "^" * (start_i - dest_i)
    horizontal = ">" * (dest_j - start_j) if dest_j > start_j else "<" * (start_j - dest_j)

    if dest_j > start_j and keypad.at(dest_i, start_j) != ".":
        return f"{vertical}{horizontal}A"

    if keypad.at(start_i, dest_j) != ".":
        return f"{horizontal}{vertical}A"

    return f"{vertical}{horizontal}A"


def get_adj_pair_counts(code: str) -> dict[tuple[str, str], int]:
    pair_counts = defaultdict(int)
    for start_key, dest_key in zip("A" + code, code):
        pair_counts[(start_key, dest_key)] += 1
    return pair_counts


def get_next_pairs(pairs: dict[tuple[str, str], int], keypad: Grid) -> dict[tuple[str, str], int]:
    next_pairs = defaultdict(int)
    for (start_key, dest_key), num in pairs.items():
        path = shortest_path(start_key, dest_key, keypad)
        for k, v in get_adj_pair_counts(path).items():
            next_pairs[k] += v * num
    return next_pairs


def len_shortest_sequence(code: str, num_directional_keypads: int) -> int:
    initial_pairs = get_adj_pair_counts(code)
    next_pairs = get_next_pairs(initial_pairs, NUMERIC_KEYPAD)
    for _ in range(num_directional_keypads):
        next_pairs = get_next_pairs(next_pairs, DIRECTIONAL_KEYPAD)
    return sum(next_pairs.values())


def get_total_complexity(puzzle_input: list[str], num_directional_keypads: int):
    res = 0
    for code in puzzle_input:
        numeric_value = int("".join([ch for ch in code if ch != "A"]))
        res += numeric_value * len_shortest_sequence(code, num_directional_keypads)
    return res


def solve_part_1(puzzle_input: list[str]):
    return get_total_complexity(puzzle_input, 2)


def solve_part_2(puzzle_input: list[str]):
    return get_total_complexity(puzzle_input, 25)
