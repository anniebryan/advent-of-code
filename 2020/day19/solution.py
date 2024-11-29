import regex
from itertools import count

filename = '2020/day19/day19.txt'
puzzle_input = open(filename).read()

def process_input():
    rules, messages = puzzle_input.split('\n\n')
    new_rules = {}
    for rule in rules.split('\n'):
        n, d = rule.split(': ')
        new_rules[int(n)] = d
    return new_rules, messages

def build_regex(rules, n, part_2):
    if part_2:
        if n == 8:  return f'({build_regex(rules, 42, True)}+)'
        if n == 11: return f'(?P<{"r0"}>{build_regex(rules, 42, True)}(?P>{"r0"})?{build_regex(rules, 31, True)})'

    rule = rules[n]
    match = regex.match(r'"(\w)"', rule)
    if match: return match.group(1)
    
    pattern = ""
    for sub_rule in rule.split(' | '):
        pattern += "".join([build_regex(rules, int(m), part_2) for m in sub_rule.split()]) + "|"
    pattern = pattern[:-1] # remove last "|"
    return f'({pattern})'

def num_that_match(rule, part_2):
    rules, messages = process_input()
    matches = regex.findall(f'^{build_regex(rules, rule, part_2)}$', messages, flags=regex.MULTILINE)
    return len(matches)

def part_1():
    return num_that_match(0, False)

def part_2():
    return num_that_match(0, True)

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))
