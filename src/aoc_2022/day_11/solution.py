"""
Advent of Code 2022
Day 11: Monkey in the Middle
"""

import os
from functools import reduce
from pathlib import Path

import click
import regex as re


class Monkey:
    def __init__(self, rows):
        self.items = [int(n) for n in re.findall("Starting items: (.*)", rows[1])[0].split(", ")]

        operation, value = re.findall(r"Operation: new = old (\*|\+) (.*)", rows[2])[0]
        op = {"+": lambda x, y: x + y, "*": lambda x, y: x * y}[operation]
        if re.match(r"\d", value):
            self.operation = lambda old: op(old, int(value))
        else:
            self.operation = lambda old: op(old, old)

        self.divisible_by = int(re.findall(r"Test: divisible by (\d+)", rows[3])[0])
        self.test = lambda n: n % self.divisible_by == 0

        self.throw_if_true = int(re.findall(r"If true: throw to monkey (\d+)", rows[4])[0])
        self.throw_if_false = int(re.findall(r"If false: throw to monkey (\d+)", rows[5])[0])

        self.num_times_inspected = 0
        self.memo = {}

    def append_item(self, item):
        self.items.append(item)

    def inspect_all_items(self, part_2, product):
        while self.items:
            item = self.items.pop(0)
            self.num_times_inspected += 1
            if item not in self.memo:
                divide_by = 1 if part_2 else 3
                worry_level = (self.operation(item) // divide_by) % product
                throw_to = self.throw_if_true if self.test(worry_level) else self.throw_if_false
                self.memo[item] = (throw_to, worry_level)
            yield self.memo[item]


def create_monkeys(puzzle_input):
    monkeys = {i: Monkey(puzzle_input[i * 7 : (i * 7) + 6]) for i in range(len(puzzle_input) // 7)}
    for i in range(0, len(puzzle_input), 7):
        monkeys[i / 7] = Monkey(puzzle_input[i:i + 6])
    return monkeys


def n_rounds(puzzle_input, n, part_2):
    monkeys = create_monkeys(puzzle_input)
    product = reduce(lambda x, y: x * y, map(lambda i: monkeys[i].divisible_by, monkeys))

    for _ in range(n):
        for i in sorted(monkeys.keys()):
            monkey = monkeys[i]
            for (thrown_to, worry_level) in monkey.inspect_all_items(part_2, product):
                monkeys[thrown_to].append_item(worry_level)
    return monkeys


def monkey_business(monkeys):
    num_inspections = map(lambda i: monkeys[i].num_times_inspected, monkeys)
    most_active = sorted(num_inspections, reverse=True)
    return most_active[0] * most_active[1]


def solve_part_1(puzzle_input: list[str]):
    monkeys = n_rounds(puzzle_input, 20, False)
    return monkey_business(monkeys)


def solve_part_2(puzzle_input: list[str]):
    monkeys = n_rounds(puzzle_input, 10000, True)
    return monkey_business(monkeys)
