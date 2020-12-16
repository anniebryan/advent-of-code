from math import prod

filename = '2020/day16/day16.txt'
puzzle_input = open(filename).readlines()

def process_input():
    i = puzzle_input.index('\n')
    fields = process_fields(puzzle_input[:i])
    tickets = puzzle_input[i+1:]
    i = tickets.index('\n')
    my_ticket = process_tickets(tickets[1:i])[0]
    nearby_tickets = process_tickets(tickets[i+2:])
    return fields, my_ticket, nearby_tickets

def process_fields(ls):
    fields = {}
    for field in ls:
        vals = set()
        name, nums = field.split(": ")
        for n in nums.split()[0::2]:
            low, high = n.split("-")
            vals |= {i for i in range(int(low), int(high)+1)}
        fields[name] = vals
    return fields

def process_tickets(ls):
    return [[int(i) for i in ticket.split(',')] for ticket in ls]

def all_valid(ticket, all_values):
    for val in ticket:
        if val not in all_values:
            return False
    return True

def get_invalid_values():
    fields, _, nearby_tickets = process_input()
    all_values = {n for s in fields.values() for n in s}
    for ticket in nearby_tickets:
        for val in ticket:
            if val not in all_values:
                yield val

def get_valid_tickets():
    fields, _, nearby_tickets = process_input()
    all_values = {n for s in fields.values() for n in s}
    return fields, [ticket for ticket in nearby_tickets if all_valid(ticket, all_values)]

def get_potential_order():
    fields, valid_tickets = get_valid_tickets()
    field_names = set(fields.keys())
    potential_orders = {i: field_names for i in range(len(valid_tickets[0]))}
    for ticket in valid_tickets:
        for i in range(len(ticket)):
            potential_orders[i] = {name for name in potential_orders[i] if ticket[i] in fields[name]}
    return potential_orders

def get_field_order():
    final_order = {}
    potential_orders = get_potential_order()
    while potential_orders:
        removed_i = set()
        fields_to_remove = set()
        for i in potential_orders:
            if len(potential_orders[i]) == 1:
                removed_i.add(i)
                field = next(iter(potential_orders[i]))
                final_order[i] = field
                fields_to_remove.add(field)
        for i in removed_i:
            if i in potential_orders:
                del potential_orders[i]
        for i in potential_orders:
            potential_orders[i] = {field for field in potential_orders[i] if field not in fields_to_remove}
    return final_order

def get_values_starting_with(word):
    final_order = get_field_order()
    fields, my_ticket, _ = process_input()
    field_names = fields.keys()
    n = len(word)
    field_names_starting = {name for name in field_names if name[:n] == word}
    for i in range(len(my_ticket)):
        if final_order[i] in field_names_starting:
            yield my_ticket[i]

def part_1():
    return sum(get_invalid_values())

def part_2():
    return prod(get_values_starting_with('departure'))

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))