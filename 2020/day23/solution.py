from math import prod

filename = '2020/day23/puzzle.txt'
puzzle_input = open(filename).read()

def get_initial_cups(num_cups):
    if num_cups is None: num_cups = len(puzzle_input)
    vals = [int(n) for n in puzzle_input]
    cups = {}
    for i in range(len(vals)-1):
        cups[vals[i]] = vals[i+1]

    cups[vals[-1]] = len(vals)+1 if num_cups > len(vals) else vals[0]

    for i in range(len(vals)+1, num_cups):
        cups[i] = i+1

    if num_cups > len(vals):
        cups[num_cups] = vals[0]
        
    return cups, vals[0]

def make_move(cups, current_cup):
    a = cups[current_cup]
    b = cups[a]
    c = cups[b]
    removed = {a, b, c}

    destination_cup = current_cup - 1 if current_cup > 1 else max(cups)
    while destination_cup in removed:
        destination_cup = destination_cup - 1 if destination_cup > 1 else max(cups)

    cups[current_cup] = cups[c]
    cups[c] = cups[destination_cup]
    cups[destination_cup] = a

    current_cup = cups[current_cup]
    return cups, current_cup

def make_n_moves(num_rounds, num_cups=None):
    cups, current_cup = get_initial_cups(num_cups)
    for _ in range(num_rounds):
        cups, current_cup = make_move(cups, current_cup)
    return cups

def list_starting_at(cups, start):
    s = ""
    cup = cups[start]
    while cup != start:
        s += str(cup)
        cup = cups[cup]
    return s

def get_clockwise(cups, start):
    a = cups[start]
    b = cups[a]
    return (a, b)

def part_1():
    cups = make_n_moves(100)
    return list_starting_at(cups, 1)

def part_2():
    cups = make_n_moves(10000000, 1000000)
    return prod(get_clockwise(cups, 1))

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))