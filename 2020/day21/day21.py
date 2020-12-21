filename = '2020/day21/day21.txt'
puzzle_input = open(filename).readlines()

def get_all_foods():
    all_ingredients = set()
    all_allergens = set()
    for food in puzzle_input:
        ingredients, allergens = food.split(' (contains ')
        ingredients = ingredients.split()
        allergens = allergens[:-2].split(', ')
        all_ingredients |= set(ingredients)
        all_allergens |= set(allergens)
    return all_ingredients, all_allergens

def get_food_list():
    food_list = []
    for food in puzzle_input:
        ingredients, allergens = food.split(' (contains ')
        ingredients = ingredients.split()
        allergens = allergens[:-2].split(', ')
        food_list.append((ingredients, allergens))
    return food_list

def get_allergen_map():
    all_ingredients, all_allergens = get_all_foods()
    food_list = get_food_list()
    allergen_map = {a: all_ingredients for a in all_allergens}
    for ingredients, allergens in food_list:
        for a in allergens:
            allergen_map[a] = {i for i in allergen_map[a] if i in ingredients}
    return allergen_map

def get_impossible_ingredients():
    all_ingredients = get_all_foods()[0]
    allergen_map = get_allergen_map()
    allergen_ingredients = set([a for s in allergen_map.values() for a in s])
    return all_ingredients.difference(allergen_ingredients)

def num_occurrences():
    impossible_ingredients = get_impossible_ingredients()
    food_list = get_food_list()
    return len([i for ingredients, allergens in food_list for i in ingredients if i in impossible_ingredients])

def get_assignments():
    allergen_map = get_allergen_map()
    assignments = {}
    while len(allergen_map) > 0:
        allergen = min(allergen_map, key=lambda x:len(allergen_map[x]))
        if len(allergen_map[allergen]) == 1:
            ingredient = next(iter(allergen_map[allergen]))
            assignments[allergen] = ingredient
            del allergen_map[allergen]
            for allergen in allergen_map:
                allergen_map[allergen] = {ing for ing in allergen_map[allergen] if ing != ingredient}
    return assignments

def alphabetize_ingredient_list():
    assignments = get_assignments()
    alphabetical_allergens = sorted(assignments)
    return ','.join(assignments[a] for a in alphabetical_allergens)

def part_1():
    return num_occurrences()

def part_2():
    return alphabetize_ingredient_list()

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))
