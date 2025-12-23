"""
Advent of Code 2023
Day 20: Pulse Propagation
"""

from collections import defaultdict, deque
from enum import Enum, auto
from math import lcm


class Pulse(Enum):
    HIGH = auto()
    LOW = auto()


class State(Enum):
    ON = auto()
    OFF = auto()


def parse_input(puzzle_input: list[str], part_2: bool):
    broadcast: list[str] = []
    flip_flop: dict[str, list[str]] = {}
    conjunction: dict[str, list[str]] = {}
    module_to_all_inputs: dict[str, set[str]] = defaultdict(set)
    for line in puzzle_input:
        module_name, dest_modules = line.split(" -> ")
        dest_modules = dest_modules.split(", ")
        if module_name == "broadcaster":
            broadcast = dest_modules
        elif module_name.startswith("%"):
            module_name = module_name[1:]
            flip_flop[module_name] = dest_modules
        elif module_name.startswith("&"):
            module_name = module_name[1:]
            conjunction[module_name] = dest_modules
        else:
            raise ValueError(f"Unexpected module name: {module_name}")
        for d in dest_modules:
            module_to_all_inputs[d].add(module_name)
    return broadcast, flip_flop, conjunction, module_to_all_inputs


def get_initial_low_pulses_received(conjunction, module_to_all_inputs):
    return {
        c: {inp: Pulse.LOW for inp in module_to_all_inputs[c]}
        for c in conjunction
    }


def press_button(broadcast, flip_flop, conjunction, state, most_recent_pulse_recieved, penultimate):
    num_low_pulses = 1  # ensure we count 'button -low-> broadcaster'
    num_high_pulses = 0
    wrote_to_penultimate = False
    q = deque([("broadcast", Pulse.LOW, b) for b in broadcast])
    while q:
        (sender, pulse, recipient) = q.popleft()
        if pulse == Pulse.LOW and recipient in penultimate:
            wrote_to_penultimate = True
        match pulse:
            case Pulse.LOW:
                num_low_pulses += 1
            case Pulse.HIGH:
                num_high_pulses += 1
        if recipient in flip_flop:
            if pulse == Pulse.LOW:
                match state[recipient]:
                    case State.ON:
                        state[recipient] = State.OFF
                        for dest in flip_flop[recipient]:
                            q.append((recipient, Pulse.LOW, dest))
                    case State.OFF:
                        state[recipient] = State.ON
                        for dest in flip_flop[recipient]:
                            q.append((recipient, Pulse.HIGH, dest))
        elif recipient in conjunction:
            most_recent_pulse_recieved[recipient][sender] = pulse
            input_pulses = list(most_recent_pulse_recieved[recipient].values())
            if all(p == Pulse.HIGH for p in input_pulses):
                for dest in conjunction[recipient]:
                    q.append((recipient, Pulse.LOW, dest))
            else:
                for dest in conjunction[recipient]:
                    q.append((recipient, Pulse.HIGH, dest))
    return num_low_pulses, num_high_pulses, state, most_recent_pulse_recieved, wrote_to_penultimate


def solve_part_1(puzzle_input: list[str]):
    broadcast, flip_flop, conjunction, module_to_all_inputs = parse_input(puzzle_input, False)

    state = {x: State.OFF for x in flip_flop}
    most_recent_pulse_recieved = get_initial_low_pulses_received(conjunction, module_to_all_inputs)

    total_low_pulses, total_high_pulses = 0, 0
    for _ in range(1000):
        num_low_pulses, num_high_pulses, state, most_recent_pulse_recieved, _ = (
            press_button(broadcast, flip_flop, conjunction, state, most_recent_pulse_recieved, set())
        )
        total_low_pulses += num_low_pulses
        total_high_pulses += num_high_pulses

    return total_low_pulses * total_high_pulses


def solve_part_2(puzzle_input: list[str]):
    broadcast, flip_flop, conjunction, module_to_all_inputs = parse_input(puzzle_input, True)

    state = {x: State.OFF for x in flip_flop}
    most_recent_pulse_recieved = get_initial_low_pulses_received(conjunction, module_to_all_inputs)

    set_writes_to_rx = module_to_all_inputs["rx"]
    assert len(set_writes_to_rx) == 1
    writes_to_rx = list(set_writes_to_rx)[0]

    penultimate_to_rx = module_to_all_inputs[writes_to_rx]
    num_penultimate = len(penultimate_to_rx)
    cycle_lengths = []

    i = 0
    while True:
        i += 1
        _, _, state, most_recent_pulse_recieved, wrote_to_penultimate = (
            press_button(broadcast, flip_flop, conjunction, state, most_recent_pulse_recieved, penultimate_to_rx)
        )
        if wrote_to_penultimate:
            cycle_lengths.append(i)
            if len(cycle_lengths) == num_penultimate:
                return lcm(*cycle_lengths)
