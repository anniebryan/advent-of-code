"""
Advent of Code 2023
Day 19: Aplenty
"""

import re
from enum import Enum, auto
from math import prod
from typing import Any

MIN_VALUE = 1
MAX_VALUE = 4_000


class Outcome(Enum):
    ACCEPT = auto()
    REJECT = auto()

    def __repr__(self) -> str:
        if self == Outcome.ACCEPT:
            return "A"
        if self == Outcome.REJECT:
            return "R"
        raise ValueError(f"Invalid Outcome: {self}")


class Rule:
    def __init__(self, rule: str):
        cond, rest = rule.split(":", 1)
        match = re.match(r"(?P<varname>[a-z])(?P<sign>[<>])(?P<threshold>\d+)", cond)
        assert match is not None
        self.varname = match.group("varname")
        self.sign = match.group("sign")
        self.threshold = int(match.group("threshold"))
        self.cond = lambda x: (x > self.threshold) if self.sign == ">" else (x < self.threshold)

        outcome_if_true, outcome_if_false = rest.split(",", 1)

        if "," in outcome_if_true:
            self.outcome_if_true = Rule(outcome_if_true)
        elif outcome_if_true == "A":
            self.outcome_if_true = Outcome.ACCEPT
        elif outcome_if_true == "R":
            self.outcome_if_true = Outcome.REJECT
        else:
            self.outcome_if_true = outcome_if_true

        if "," in outcome_if_false:
            self.outcome_if_false = Rule(outcome_if_false)
        elif outcome_if_false == "A":
            self.outcome_if_false = Outcome.ACCEPT
        elif outcome_if_false == "R":
            self.outcome_if_false = Outcome.REJECT
        else:
            self.outcome_if_false = outcome_if_false
    
    def __repr__(self) -> str:
        return (
            f"Rule({self.varname}{self.sign}{self.threshold}:"
            + f"{repr(self.outcome_if_true)},"
            + f"{repr(self.outcome_if_false)})"
        )

    def execute(self, **kwargs: Any) -> str | Outcome:
        """Returns either an outcome (accept/reject) or the name of the next workflow to run."""
        value = kwargs[self.varname]
        outcome = self.outcome_if_true if self.cond(value) else self.outcome_if_false
        if isinstance(outcome, Outcome):
            return outcome
        if isinstance(outcome, Rule):
            return outcome.execute(**kwargs)
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


def num_combinations_accepted(
        rules: dict[str, Rule],
        rule: Rule,
        x_min: int = MIN_VALUE,
        x_max: int = MAX_VALUE,
        m_min: int = MIN_VALUE,
        m_max: int = MAX_VALUE,
        a_min: int = MIN_VALUE,
        a_max: int = MAX_VALUE,
        s_min: int = MIN_VALUE,
        s_max: int = MAX_VALUE,
) -> int:
    num_combinations = 0

    kwargs = dict(x_min=x_min, x_max=x_max, m_min=m_min, m_max=m_max, a_min=a_min, a_max=a_max, s_min=s_min, s_max=s_max)
    min_vals = {"x": x_min, "m": m_min, "a": a_min, "s": s_min}
    max_vals = {"x": x_max, "m": m_max, "a": a_max, "s": s_max}

    min_val = min_vals[rule.varname]
    max_val = max_vals[rule.varname]

    if rule.outcome_if_true != Outcome.REJECT:
        if rule.sign == "<":
            new_min_val = min_val
            new_max_val = min(max_val, rule.threshold) - 1
        else:
            new_min_val = max(min_val, rule.threshold) + 1
            new_max_val = max_val
        n = max(new_max_val - new_min_val + 1, 0)
        kwargs[f"{rule.varname}_min"] = new_min_val
        kwargs[f"{rule.varname}_max"] = new_max_val

        if n > 0:
            if rule.outcome_if_true == Outcome.ACCEPT:
                num_combinations += n * prod(max(max_vals[v] - min_vals[v] + 1, 0) for v in "xmas" if v != rule.varname)
            elif isinstance(rule.outcome_if_true, Rule):
                num_combinations += num_combinations_accepted(rules, rule.outcome_if_true, **kwargs)
            else:
                num_combinations += num_combinations_accepted(rules, rules[rule.outcome_if_true], **kwargs)

    if rule.outcome_if_false != Outcome.REJECT:
        if rule.sign == "<":
            new_min_val = max(min_val, rule.threshold)
            new_max_val = max_val
        else:
            new_min_val = min_val
            new_max_val = min(max_val, rule.threshold)
        n = max(new_max_val - new_min_val + 1, 0)
        kwargs[f"{rule.varname}_min"] = new_min_val
        kwargs[f"{rule.varname}_max"] = new_max_val

        if n > 0:
            if rule.outcome_if_false == Outcome.ACCEPT:
                num_combinations += n * prod(max(max_vals[v] - min_vals[v] + 1, 0) for v in "xmas" if v != rule.varname)
            elif isinstance(rule.outcome_if_false, Rule):
                num_combinations += num_combinations_accepted(rules, rule.outcome_if_false, **kwargs)
            elif rule.outcome_if_false != Outcome.REJECT:
                num_combinations += num_combinations_accepted(rules, rules[rule.outcome_if_false], **kwargs)

    return num_combinations


def solve_part_1(puzzle_input: list[str]):
    rules, all_parts = parse_input(puzzle_input, False)
    total_rating = 0
    for part in all_parts:
        if part_is_accepted(part, rules, "in"):
            total_rating += sum(part.values())
    return total_rating


def solve_part_2(puzzle_input: list[str]):
    rules, _ = parse_input(puzzle_input, True)
    return num_combinations_accepted(rules, rules["in"])
