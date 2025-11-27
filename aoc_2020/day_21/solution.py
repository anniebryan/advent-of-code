"""
Advent of Code 2020
Day 21: Allergen Assessment
"""

import click
import os
from pathlib import Path


def get_all_foods(puzzle_input):
    all_ingredients = set()
    all_allergens = set()
    for food in puzzle_input:
        ingredients, allergens = food.split(' (contains ')
        all_ingredients |= set(ingredients.split())
        all_allergens |= set(allergens[:-1].split(', '))
    return all_ingredients, all_allergens


def get_food_list(puzzle_input):
    food_list = []
    for food in puzzle_input:
        ingredients, allergens = food.split(' (contains ')
        food_list.append((ingredients.split(), allergens[:-1].split(', ')))
    return food_list


def get_allergen_map(puzzle_input):
    all_ingredients, all_allergens = get_all_foods(puzzle_input)
    food_list = get_food_list(puzzle_input)
    allergen_map = {a: all_ingredients for a in all_allergens}
    for ingredients, allergens in food_list:
        for a in allergens:
            allergen_map[a] = {i for i in allergen_map[a] if i in ingredients}
    return allergen_map


def get_impossible_ingredients(puzzle_input):
    all_ingredients = get_all_foods(puzzle_input)[0]
    allergen_ingredients = set([a for s in get_allergen_map(puzzle_input).values() for a in s])
    return all_ingredients.difference(allergen_ingredients)


def num_occurrences(puzzle_input):
    impossible_ingredients = get_impossible_ingredients(puzzle_input)
    food_list = get_food_list(puzzle_input)
    return len([i for ingredients, allergens in food_list for i in ingredients if i in impossible_ingredients])


def get_assignments(puzzle_input):
    allergen_map = get_allergen_map(puzzle_input)
    assignments = {}
    while len(allergen_map) > 0:
        allergen = min(allergen_map, key=lambda x:len(allergen_map[x]))
        ingredient = next(iter(allergen_map[allergen]))
        assignments[allergen] = ingredient
        del allergen_map[allergen]
        for allergen in allergen_map:
            allergen_map[allergen] = {ing for ing in allergen_map[allergen] if ing != ingredient}
    return assignments


def alphabetize_ingredient_list(puzzle_input):
    assignments = get_assignments(puzzle_input)
    alphabetical_allergens = sorted(assignments)
    return ','.join(assignments[a] for a in alphabetical_allergens)


def solve_part_1(puzzle_input: list[str]):
    return num_occurrences(puzzle_input)


def solve_part_2(puzzle_input: list[str]):
    return alphabetize_ingredient_list(puzzle_input)


@click.command()
@click.option("-se", "--skip_example", is_flag=True, default=False)
@click.option("-sp", "--skip_puzzle", is_flag=True, default=False)
def main(skip_example: bool = False, skip_puzzle: bool = False) -> None:
    base_dir = Path(__file__).parent
    example_files = sorted([fn for fn in os.listdir(base_dir) if fn.endswith(".txt") and "example" in fn])

    def _run_solution(filename: str, display_name: str):
        print(f"--- {display_name} ---")

        if not (filepath := (base_dir / filename)).exists():
            print(f"{filename} not found.")
            return

        with open(filepath) as file:
            puzzle_input = [line.strip("\n") for line in file]
            print(f"Part 1: {solve_part_1(puzzle_input)}")
            print(f"Part 2: {solve_part_2(puzzle_input)}")
        return

    if not skip_example:
        if len(example_files) < 2:
            _run_solution("example.txt", "Example")
        else:
            for i, filename in enumerate(example_files):
                _run_solution(filename, f"Example {i + 1}")

    if not skip_puzzle:
        _run_solution("puzzle.txt", "Puzzle")


if __name__ == "__main__":
    main()
