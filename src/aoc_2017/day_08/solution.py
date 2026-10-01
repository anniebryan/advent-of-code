"""
Advent of Code 2017
Day 8: I Heard You Like Registers
"""

from typing import Literal


class Register:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    def apply_delta(self, delta: int) -> None:
        self.value += delta


class Condition:
    def __init__(self, register_name: str, op: str, value: int):
        self.register_name = register_name
        self.op = op
        self.value = value

    def evaluate(self, registers: dict[str, Register]) -> bool:
        register = registers[self.register_name]
        actual_value = register.value
        fn = {
            "<": lambda x, y: x < y,
            ">": lambda x, y: x > y,
            "<=": lambda x, y: x <= y,
            ">=": lambda x, y: x >= y,
            "==": lambda x, y: x == y,
            "!=": lambda x, y: x != y,
        }[self.op]
        return fn(actual_value, self.value)


class Instruction:
    def __init__(
        self,
        register_name_to_change: str,
        inc_or_dec: Literal["inc", "dec"],
        amount: int,
        cond: Condition,
    ):
        self.register_name_to_change = register_name_to_change
        self.delta = amount * {"inc": 1, "dec": -1}[inc_or_dec]
        self.cond = cond


def parse_input(puzzle_input: list[str]):
    registers: dict[str, Register] = {}
    instructions: list[Instruction] = []

    for line in puzzle_input:
        parts = line.split()
        assert len(parts) == 7
        register_name_to_change, inc_or_dec, amount, _if, cond_register_name, op, value = parts

        for reg_name in (register_name_to_change, cond_register_name):
            if reg_name not in registers:
                register = Register(reg_name, 0)
                registers[reg_name] = register

        assert inc_or_dec in {"inc", "dec"}
        assert _if == "if"

        cond = Condition(cond_register_name, op, int(value))
        instruction = Instruction(register_name_to_change, inc_or_dec, int(amount), cond)
        instructions.append(instruction)

    return registers, instructions


def solve_part_1(puzzle_input: list[str]):
    registers, instructions = parse_input(puzzle_input)
    for i in instructions:
        if i.cond.evaluate(registers):
            registers[i.register_name_to_change].apply_delta(i.delta)
    return max(r.value for r in registers.values())


def solve_part_2(puzzle_input: list[str]):
    registers, instructions = parse_input(puzzle_input)
    max_val = max(r.value for r in registers.values())
    for i in instructions:
        if i.cond.evaluate(registers):
            registers[i.register_name_to_change].apply_delta(i.delta)
            max_val = max(max_val, max(r.value for r in registers.values()))
    return max_val
