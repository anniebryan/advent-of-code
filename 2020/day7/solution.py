import re
from collections import defaultdict
from collections import deque

filename = '2020/day7/puzzle.txt'
puzzle_input = open(filename).readlines()

def get_containers():
    """ returns a dictionary that maps a string to a set of strings
    with all bags that can contain that string """
    containers = defaultdict(set)
    for rule in puzzle_input:
        outer_bag = re.match('([A-Za-z ]+) bags', rule)[1]
        inner_bags = re.findall(r'(\d+) ([A-Za-z ]+?) bags?', rule)
        for bag in inner_bags:
            containers[bag[1]].add(outer_bag)
    return containers

def get_num_containing():
    """ returns a dictionary that maps a string to a set of tuples (n, b)
    such that the key must contain n bags of type b """
    containing = {}
    for rule in puzzle_input:
        outer_bag = re.match(r'([A-Za-z ]+) bags', rule)[1].split(" bags contain no other")[0]
        inner_bags = re.findall(r'(\d+) ([A-Za-z ]+?) bags?', rule)
        containing[outer_bag] = {(int(t[0]), t[1]) for t in inner_bags}
    return containing

def get_all_possible_containers(color):
    containers = get_containers()
    possible = set()
    seen = set()
    queue = deque()
    queue.append(color)
    while queue:
        c = queue.pop()
        for container in containers[c]:
            if container not in seen: # prevents cycles
                possible.add(container)
                seen.add(container)
                queue.append(container)
    return possible

def get_total_num_containing(color, containing):
    num_containing = 0
    for t in containing[color]:
        num_containing += t[0]*(1 + get_total_num_containing(t[1], containing))
    return num_containing

def part_1():
    return len(get_all_possible_containers('shiny gold'))

def part_2():
    return get_total_num_containing('shiny gold', get_num_containing())

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))