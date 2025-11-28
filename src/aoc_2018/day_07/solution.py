"""
Advent of Code 2018
Day 7: The Sum of Its Parts
"""

import copy
import os
from collections import defaultdict
from pathlib import Path

import click
import regex as re


def parse_requirements(puzzle_input):
    requirements = {
        re.findall(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin', i)[0]
        for i in puzzle_input
    }
    all_steps = {r[i] for r in requirements for i in [0, 1]}
    all_prerequisites = defaultdict(set)
    all_dependencies = defaultdict(set)
    for s1, s2 in requirements:
        all_prerequisites[s2].add(s1)
        all_dependencies[s1].add(s2)
    return all_steps, all_prerequisites, all_dependencies


def get_available(steps, completed, prerequisites):
    """
    returns a set of steps that have not been completed and have all prerequisites fulfilled
    """
    remaining = steps - completed
    available = {r for r in remaining if prerequisites[r] == set()}
    return available


def update_prerequisites(prerequisites, dependencies, step):
    """
    prerequisites: dictionary mapping a step to a set of ts prerequisites
    dependencies: dictionary mapping step to a set of steps that depend on it
    step: the step being completed
    returns an updated prerequisite dictionary removing the step being completed
    """
    updated = copy.deepcopy(prerequisites)
    for s in dependencies[step]:
        if step in updated[s]:
            updated[s].remove(step)
    return updated


def solve_part_1(puzzle_input: list[str]):
    """
    returns an order for steps to be completed satisfying all prerequisites as given in day7.txt
    ties are broken alphabetically
    """
    all_steps, all_prerequisites, all_dependencies = parse_requirements(puzzle_input[2:])
    steps, prerequisites = copy.deepcopy(all_steps), copy.deepcopy(all_prerequisites)
    completed = set()
    order = []
    while len(completed) < len(steps):
        available = get_available(steps, completed, prerequisites)
        order.append(min(available))
        completed.add(min(available))
        prerequisites = update_prerequisites(prerequisites, all_dependencies, min(available))
    return "".join(order)


def get_required_duration(c, seconds_to_subtract):
    """
    :return: integer duration of time
    >>> get_required_duration('A')
    61
    >>> get_required_duration('Z')
    86
    """
    return ord(c) - 4 - seconds_to_subtract


def timestep(workers, completed, prerequisites, all_steps, all_dependencies, seconds_to_subtract):
    """
    symbolizes the passage of one step of time
    """
    for w, s in workers.items():
        if s is not None:
            workers[w] = (s[0], s[1]-1)
            if workers[w][1] == 0:  # completed step
                workers[w] = None
                completed.add(s[0])
                prerequisites = update_prerequisites(prerequisites, all_dependencies, s[0])
    available_workers = {w for w in workers if not workers[w]}
    being_completed = {workers[w][0] for w in workers if workers[w] is not None}
    available_steps = get_available(all_steps, completed.union(being_completed), prerequisites)
    while available_workers and available_steps:
        w = min(available_workers)
        s = min(available_steps)
        workers[w] = (s, get_required_duration(s, seconds_to_subtract))
        available_workers = {w for w in workers if not workers[w]}
        being_completed = {workers[w][0] for w in workers if workers[w] is not None}
        available_steps = get_available(all_steps, completed.union(being_completed), prerequisites)
    return workers, completed, prerequisites


def solve_part_2(puzzle_input: list[str]):
    """
    returns the amount of time required to complete all the steps
    given durations as described in get_required_duration
    ties are broken alphabetically
    """
    num_workers = int(puzzle_input[0])
    seconds_to_subtract = int(puzzle_input[1])
    all_steps, all_prerequisites, all_dependencies = parse_requirements(puzzle_input[2:])
    # maps worker -> None if idle
    # maps worker -> (step, time remaining) otherwise
    workers = dict.fromkeys(range(num_workers))
    completed = set()
    time = 0
    _, prerequisites = copy.deepcopy(all_steps), copy.deepcopy(all_prerequisites)
    while len(completed) < len(all_steps):
        workers, completed, prerequisites = timestep(
            workers,
            completed,
            prerequisites,
            all_steps,
            all_dependencies,
            seconds_to_subtract,
        )
        time += 1
    return time - 1
