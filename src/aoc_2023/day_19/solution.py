"""
Advent of Code 2023
Day 19: Aplenty
"""

import ast
import copy
import heapq
import operator
import os
import re
import string
import sys
from collections import Counter, defaultdict, deque
from collections.abc import Iterator
from enum import Enum, auto
from functools import cmp_to_key, lru_cache, reduce
from itertools import combinations, cycle
from math import lcm, prod
from pathlib import Path
from statistics import median
from typing import Any, Callable, Iterable, Iterator, Literal

import click
import numpy
import regex

from aoc_utils import DirectedGraph, DirectedWeightedGraph, Grid, IntRangeMap, IntRangeSet

MIN_VALUE = 1
MAX_VALUE = 4_000


class Outcome(Enum):
    ACCEPT = auto()
    REJECT = auto()


class Rule:
    def __init__(self, rule: str):
        cond, rest = rule.split(":", 1)
        match = re.match(r"(?P<varname>[a-z])(?P<sign>[<>])(?P<threshold>\d+)", cond)
        assert match is not None
        self.varname = match.group("varname")
        self.sign = match.group("sign")
        self.threshold = int(match.group("threshold"))
        self.cond = lambda x: (x > self.threshold) if self.sign == ">" else (x < self.threshold)
        self.outcome_if_true, self.outcome_if_false = rest.split(",", 1)

    def execute(self, **kwargs: Any) -> str | Outcome:
        """Returns either an outcome (accept/reject) or the name of the next workflow to run."""
        value = kwargs[self.varname]
        outcome = self.outcome_if_true if self.cond(value) else self.outcome_if_false
        if outcome == "A":
            return Outcome.ACCEPT
        if outcome == "R":
            return Outcome.REJECT
        if "," in outcome:
            return Rule(outcome).execute(**kwargs)
        return outcome


def parse_input(puzzle_input: list[str], part_2: bool) -> tuple[dict[str, Rule], list[dict[str, int]]]:
    rules = {}
    for i, line in enumerate(puzzle_input):
        if line == "":
            break
        match = re.match(r"(?P<name>.*)\{(?P<rule>.*)\}", line)
        assert match is not None
        workflow_name = match.group("name")
        rules[workflow_name] = Rule(match.group("rule"))

    all_parts = []
    for line in puzzle_input[i + 1:]:
        parts = {}
        for part in line[1:-1].split(","):
            part_name, rating = part.split("=")
            parts[part_name] = int(rating)
        all_parts.append(parts)

    return rules, all_parts


def part_is_accepted(part: dict[str, int], rules: dict[str, Rule], rule_name: str) -> bool:
    rule = rules[rule_name]
    outcome = rule.execute(**part)
    if outcome == Outcome.ACCEPT:
        return True
    if outcome == Outcome.REJECT:
        return False
    return part_is_accepted(part, rules, outcome)


def solve_part_1(puzzle_input: list[str]):
    rules, all_parts = parse_input(puzzle_input, False)
    total_rating = 0
    for part in all_parts:
        if part_is_accepted(part, rules, "in"):
            total_rating += sum(part.values())
    return total_rating


def solve_part_2(puzzle_input: list[str]):
    rules, _ = parse_input(puzzle_input, True)
    return
