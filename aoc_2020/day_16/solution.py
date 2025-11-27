"""
Advent of Code 2020
Day 16: Ticket Translation
"""

import os
from math import prod
from pathlib import Path

import click


def process_input(puzzle_input):
    i = puzzle_input.index("")
    fields = process_fields(puzzle_input[:i])
    tickets = puzzle_input[i + 1:]
    i = tickets.index("")
    my_ticket = process_tickets(tickets[1:i])[0]
    nearby_tickets = process_tickets(tickets[i + 2:])
    return fields, my_ticket, nearby_tickets


def process_fields(ls):
    fields = {}
    for field in ls:
        vals = set()
        name, nums = field.split(": ")
        for n in nums.split()[0::2]:
            low, high = n.split("-")
            vals |= {i for i in range(int(low), int(high) + 1)}
        fields[name] = vals
    return fields


def process_tickets(ls):
    return [[int(i) for i in ticket.split(',')] for ticket in ls]


def all_valid(ticket, all_values):
    for val in ticket:
        if val not in all_values:
            return False
    return True


def get_invalid_values(puzzle_input):
    fields, _, nearby_tickets = process_input(puzzle_input)
    all_values = {n for s in fields.values() for n in s}
    for ticket in nearby_tickets:
        for val in ticket:
            if val not in all_values:
                yield val


def get_valid_tickets(puzzle_input):
    fields, _, nearby_tickets = process_input(puzzle_input)
    all_values = {n for s in fields.values() for n in s}
    return fields, [ticket for ticket in nearby_tickets if all_valid(ticket, all_values)]


def get_potential_order(puzzle_input):
    fields, valid_tickets = get_valid_tickets(puzzle_input)
    field_names = set(fields.keys())
    potential_orders = {i: field_names for i in range(len(valid_tickets[0]))}
    for ticket in valid_tickets:
        for i in range(len(ticket)):
            potential_orders[i] = {name for name in potential_orders[i] if ticket[i] in fields[name]}
    return potential_orders


def get_field_order(puzzle_input):
    final_order = {}
    potential_orders = get_potential_order(puzzle_input)
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


def get_values_starting_with(puzzle_input, word):
    final_order = get_field_order(puzzle_input)
    fields, my_ticket, _ = process_input(puzzle_input)
    field_names = fields.keys()
    n = len(word)
    field_names_starting = {name for name in field_names if name[:n] == word}
    for i in range(len(my_ticket)):
        if final_order[i] in field_names_starting:
            yield my_ticket[i]


def solve_part_1(puzzle_input: list[str]):
    return sum(get_invalid_values(puzzle_input))


def solve_part_2(puzzle_input: list[str]):
    return prod(get_values_starting_with(puzzle_input, 'departure'))


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
