"""
Advent of Code 2022
Day 19: Not Enough Minerals
"""

import re
from collections import deque

class Blueprint:
    def __init__(self, row):
        values = re.match("Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.", row).groups()
        self.id = int(values[0])
        self.ore_robot_cost = int(values[1])
        self.clay_robot_cost = int(values[2])
        self.obsidian_robot_cost = (int(values[3]), int(values[4]))
        self.geode_robot_cost = (int(values[5]), int(values[6]))


def parse(puzzle_input):
    for row in puzzle_input:
        yield Blueprint(row)


def neighbors(blueprint: Blueprint, materials, robots, prev_skipped, time_remaining):
    (ore, clay, obsidian, _) = materials
    (ore_robots, clay_robots, obsidian_robots, _) = robots
    new_values = tuple([i + j for (i, j) in zip(materials, robots)])
    new_ore, new_clay, new_obsidian, new_geode = new_values

    can_afford_ore_robot = (ore >= blueprint.ore_robot_cost)
    can_afford_clay_robot = (ore >= blueprint.clay_robot_cost)
    can_afford_obsidian_robot = (ore >= blueprint.obsidian_robot_cost[0] and clay >= blueprint.obsidian_robot_cost[1])
    can_afford_geode_robot = (ore >= blueprint.geode_robot_cost[0] and obsidian >= blueprint.geode_robot_cost[1])

    (skipped_obsidian, skipped_clay, skipped_ore) = prev_skipped

    # option 1: buy nothing
    if time_remaining == 1 or not can_afford_geode_robot:
        new_materials = (new_ore, new_clay, new_obsidian, new_geode)
        skipped = (can_afford_obsidian_robot, can_afford_clay_robot, can_afford_ore_robot)
        yield (new_materials, robots, skipped)

    # option 2: buy geode robot
    if time_remaining > 1 and can_afford_geode_robot:
        new_materials = tuple([i - j for (i, j) in zip(new_values, (blueprint.geode_robot_cost[0], 0, blueprint.geode_robot_cost[1], 0))])
        new_robots = tuple([i + j for (i, j) in zip(robots, (0, 0, 0, 1))])
        skipped = (False,) * 3
        yield (new_materials, new_robots, skipped)

    # option 3: buy obsidian robot
    if time_remaining > 2 and can_afford_obsidian_robot and not skipped_obsidian and not can_afford_geode_robot and obsidian_robots < blueprint.geode_robot_cost[1]:
        new_materials = tuple([i - j for (i, j) in zip(new_values, (blueprint.obsidian_robot_cost[0], blueprint.obsidian_robot_cost[1], 0, 0))])
        new_robots = tuple([i + j for (i, j) in zip(robots, (0, 0, 1, 0))])
        skipped = (False,) * 3
        yield (new_materials, new_robots, skipped)

    # option 4: buy clay robot
    if time_remaining > 3 and can_afford_clay_robot and not skipped_clay and not can_afford_geode_robot and not can_afford_obsidian_robot and clay_robots < blueprint.obsidian_robot_cost[1]:
        new_materials = tuple([i - j for (i, j) in zip(new_values, (blueprint.clay_robot_cost, 0, 0, 0))])
        new_robots = tuple([i + j for (i, j) in zip(robots, (0, 1, 0, 0))])
        skipped = (False,) * 3
        yield (new_materials, new_robots, skipped)

    # option 5: buy ore robot
    if time_remaining > 2 and can_afford_ore_robot and not skipped_ore and not can_afford_geode_robot and not can_afford_obsidian_robot and ore_robots < max(blueprint.ore_robot_cost, blueprint.clay_robot_cost, blueprint.obsidian_robot_cost[0], blueprint.geode_robot_cost[0]):
        new_materials = tuple([i - j for (i, j) in zip(new_values, (blueprint.ore_robot_cost, 0, 0, 0))])
        new_robots = tuple([i + j for (i, j) in zip(robots, (1, 0, 0, 0))])
        skipped = (False,) * 3
        yield (new_materials, new_robots, skipped)


def max_num_geodes(blueprint: Blueprint, init_materials, init_robots, total_time):
    queue = deque()
    seen = set()

    init_skipped = (False,) * 3
    key = (init_materials, init_robots, init_skipped, total_time)
    queue.append(([], key))
    seen.add(key)

    max_geodes = 0
    best_path = None
    while queue:
        prev, (materials, robots, skipped, t) = queue.popleft()

        if t == 0:
            geodes = materials[3]
            if geodes > max_geodes:
                max_geodes = geodes
                best_path = prev
            continue

        for neighbor in neighbors(blueprint, materials, robots, skipped, t):
            (neighbor_materials, neighbor_robots, neighbor_skipped) = neighbor
            key = (neighbor_materials, neighbor_robots, neighbor_skipped, t - 1)
            if key not in seen:
                queue.append((prev + [key], key))
                seen.add(key)

    return max_geodes, best_path


def part_1(puzzle_input):
    quality = []
    for blueprint in parse(puzzle_input):
        max_geodes, _ = max_num_geodes(blueprint, (0, 0, 0, 0), (1, 0, 0, 0), 24)
        quality.append(max_geodes * blueprint.id)
    return sum(quality)
    
def part_2(puzzle_input):
    product = 1
    for blueprint in parse(puzzle_input[:3]):
        max_geodes, _ = max_num_geodes(blueprint, (0, 0, 0, 0), (1, 0, 0, 0), 32)
        product *= max_geodes
    return product
