"""
Advent of Code 2025
Day 5: Cafeteria
"""

from aoc_utils import IntRangeSet


def parse_input(puzzle_input: list[str], part_2: bool):
    fresh_ingredients = IntRangeSet()
    ingredient_ids = []

    for i, line in enumerate(puzzle_input):
        if line == "":
            break
        a, b = map(int, line.split("-"))
        fresh_ingredients.add_range(a, b - a)

    for j, line in enumerate(puzzle_input[i + 1:]):
        ingredient_ids.append(int(line))
        line = puzzle_input[j]

    return fresh_ingredients, ingredient_ids


def solve_part_1(puzzle_input: list[str]):
    fresh_ingredients, ingredient_ids = parse_input(puzzle_input, False)
    return len([i for i in ingredient_ids if fresh_ingredients.in_range(i)])


def solve_part_2(puzzle_input: list[str]):
    fresh_ingredients, _ = parse_input(puzzle_input, True)
    return fresh_ingredients.num_values
