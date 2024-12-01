"""
Advent of Code 2022
Day 10: Cathode-Ray Tube
"""

import re


def execute_program(puzzle_input):
    register = 1
    cycle = 0
    prev_cycle_instr = None
    for row in puzzle_input:
        ready = False
        while not ready:
            # initiate a new cycle
            cycle += 1

            # yield cycle number and register value
            yield cycle, register

            # add value to register
            if prev_cycle_instr is not None:
                register += prev_cycle_instr
                prev_cycle_instr = None
            else:
                ready = True

        # parse a new row's instruction
        if re.match("addx -?(\d+)", row):
            prev_cycle_instr = int(row.split(" ")[1])
        elif row == "noop":
            prev_cycle_instr = None
        else:
            print(f"Cannot parse instruction: {row}")
        

def part_1(puzzle_input):
    cycles_of_interest = {20, 60, 100, 140, 180, 220}
    total = 0
    for cycle, register in execute_program(puzzle_input):
        if cycle in cycles_of_interest:
            total += cycle * register
    return total


def part_2(puzzle_input):
    s = ["\n"]
    for cycle, register in execute_program(puzzle_input):
        sprite = {register - 1, register, register + 1}
        ix = (cycle - 1) % 40
        if ix in sprite:
            s.append("#")
        else:
            s.append(".")
        if cycle % 40 == 0:
            s.append("\n")
    return "".join(s)
