"""
Advent of Code 2020
Day 21: Allergen Assessment
"""

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


def part_1(puzzle_input):
    return num_occurrences(puzzle_input)


def part_2(puzzle_input):
    return alphabetize_ingredient_list(puzzle_input)
