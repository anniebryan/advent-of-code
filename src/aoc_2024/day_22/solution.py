"""
Advent of Code 2024
Day 22: Monkey Market
"""

import os
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import click

N_SECRET_NUMS = 2000


def parse_input(puzzle_input: list[str]):
    return [int(n) for n in puzzle_input]


def mix(secret_number: int, res: int) -> int:
    return secret_number ^ res


def prune(secret_number: int) -> int:
    return secret_number % 16777216


def calc_next_secret_number(secret_number: int) -> int:
    secret_number = prune(mix(secret_number, secret_number * 64))
    secret_number = prune(mix(secret_number, int(secret_number / 32)))
    secret_number = prune(mix(secret_number, secret_number * 2048))
    return secret_number


def solve_part_1(puzzle_input: list[str]):
    tot = 0
    for secret_number in parse_input(puzzle_input):
        for _ in range(N_SECRET_NUMS):
            secret_number = calc_next_secret_number(secret_number)
        tot += secret_number
    return tot


def solve_part_2(puzzle_input: list[str]):
    change_to_sales = defaultdict(int)
    for secret_number in parse_input(puzzle_input):
        prices = []
        for _ in range(N_SECRET_NUMS):
            secret_number = calc_next_secret_number(secret_number)
            price = secret_number % 10
            prices.append(price)

        last_4_changes = tuple()
        seen_changes = set()
        for (prev_price, price) in zip(prices, prices[1:]):
            change = price - prev_price
            if len(last_4_changes) == 4:
                last_4_changes = (*last_4_changes[1:], change)
            else:
                last_4_changes = (*last_4_changes, change)

            if len(last_4_changes) == 4 and last_4_changes not in seen_changes:
                seen_changes.add(last_4_changes)
                change_to_sales[last_4_changes] += price

    return max(change_to_sales.values())
