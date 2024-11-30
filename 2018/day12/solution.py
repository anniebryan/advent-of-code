# Day 12: Subterranean Sustainability


def get_initial_plant_indices(puzzle_input):
    initial_state = puzzle_input[0].split()[-1]
    indices = {i for i in range(len(initial_state)) if initial_state[i] == '#'}
    return indices

def get_rules(puzzle_input):
    rules = puzzle_input[2:]
    rule_map = {}
    for rule in rules:
        key, _, val = rule.split()
        rule_map[key] = val
    return rule_map

def time_step(indices, rules):
    new_indices = set()
    for i in range(min(indices)-1, max(indices)+2):
        s = ''
        for j in range(5):
            if i+j-2 in indices:
                s += '#'
            else:
                s += '.'
        if rules[s] == '#':
            new_indices.add(i)
    return new_indices

def run_n_generations(puzzle_input, n):
    indices = get_initial_plant_indices(puzzle_input)
    rules = get_rules(puzzle_input)
    for _ in range(n):
        indices = time_step(indices, rules)
    return indices

def part_1(puzzle_input):
    return sum(run_n_generations(puzzle_input, 20))


def part_2(puzzle_input):
    return sum(run_n_generations(puzzle_input, 2000)) + (50000000000-2000)*75
