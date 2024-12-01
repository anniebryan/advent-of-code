"""
Advent of Code 2020
Day 19: Monster Messages
"""

import regex


def process_input(puzzle_input):
    ix = puzzle_input.index("")
    rules = puzzle_input[:ix]
    messages = puzzle_input[ix + 1:]
    new_rules = {}
    for rule in rules:
        n, d = rule.split(': ')
        new_rules[int(n)] = d
    return new_rules, messages


def build_regex(rules, n, part_2):
    if part_2:
        if n == 8:
            return f'({build_regex(rules, 42, True)}+)'
        if n == 11:
            return f'(?P<{"r0"}>{build_regex(rules, 42, True)}(?P>{"r0"})?{build_regex(rules, 31, True)})'

    rule = rules[n]
    match = regex.match(r'"(\w)"', rule)
    if match:
        return match.group(1)
    
    pattern = []
    for sub_rule in rule.split(' | '):
        pattern.append("".join([build_regex(rules, int(m), part_2) for m in sub_rule.split()]))
    return f"({'|'.join(pattern)})"


def num_that_match(rules, messages, part_2):
    num_matches = 0
    for m in messages:
        if regex.match(f'^{build_regex(rules, 0, part_2)}$', m):
            num_matches += 1
    return num_matches


def part_1(puzzle_input):
    rules, messages = process_input(puzzle_input)
    return num_that_match(rules, messages, False)


def part_2(puzzle_input):
    rules, messages = process_input(puzzle_input)
    return num_that_match(rules, messages, True)
