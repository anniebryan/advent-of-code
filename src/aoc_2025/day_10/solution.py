"""
Advent of Code 2025
Day 10: Factory
"""

import ast

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


def parse_input(puzzle_input: list[str], part_2: bool):
    machines = []
    for line in puzzle_input:
        indicator_lights = line.split()[0][1:-1]
        buttons = [ast.literal_eval(b) for b in line.split()[1:-1]]
        buttons = [tuple([b]) if isinstance(b, int) else b for b in buttons]
        joltage_reqs = tuple([int(v) for v in line.split()[-1][1:-1].split(",")])
        machines.append((indicator_lights, buttons, joltage_reqs))
    return machines


def fewest_button_presses_part_1(indicator_lights: str, buttons: set[tuple[int, ...]], memo: dict = {}) -> float:
    memo_key = (indicator_lights, tuple(sorted(buttons)))
    if memo_key not in memo:
        if all(ch == "." for ch in indicator_lights):
            memo[memo_key] = 0
        elif len(buttons) == 0:
            memo[memo_key] = np.inf
        else:
            options = []
            for b in buttons:
                new_lights = "".join(
                    ch if i not in b else {".": "#", "#": "."}[ch]
                    for i, ch in enumerate(indicator_lights)
                )
                new_buttons = buttons - {b}  # will never need to press the same button twice
                options.append(1 + fewest_button_presses_part_1(new_lights, new_buttons, memo))
            memo[memo_key] = min(options)
    return memo[memo_key]


def fewest_button_presses_part_2(joltage_reqs: tuple[int, ...], buttons: list[tuple[int, ...]], memo: dict = {}) -> float:
    # solve Ax = b where A describes buttons and b describes joltage reqs
    m, n = len(joltage_reqs), len(buttons)
    A = np.array([[1 if i in button else 0 for i in range(m)] for button in buttons], dtype=int).T
    b = np.array(joltage_reqs, dtype=int)
    res = milp(
        c=np.ones(n, dtype=float),  # minimize sum of resulting vector
        constraints=LinearConstraint(A, b, b),
        integrality=np.ones(n),  # all values must be integers
        bounds = Bounds(0, np.inf, True),  # all values must be >= 0
    )
    return int(res.x.sum())


def solve_part_1(puzzle_input: list[str]):
    machines = parse_input(puzzle_input, False)
    total_presses = 0
    for (indicator_lights, buttons, _) in machines:
        total_presses += fewest_button_presses_part_1(indicator_lights, set(buttons))
    return total_presses


def solve_part_2(puzzle_input: list[str]):
    machines = parse_input(puzzle_input, True)
    total_presses = 0
    for (_, buttons, joltage_reqs) in machines:
        total_presses += fewest_button_presses_part_2(joltage_reqs, buttons)
    return total_presses
