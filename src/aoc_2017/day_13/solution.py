"""
Advent of Code 2017
Day 13: Packet Scanners
"""

def parse_input(puzzle_input: list[str]):
    firewall_ranges = {}
    for line in puzzle_input:
        line_parts = line.split(": ")
        if len(line_parts) != 2:
            raise ValueError
        firewall_ranges[int(line_parts[0])] = int(line_parts[1])
    return firewall_ranges


def _scanner_loc(layer_range: int, i: int) -> int:
    i %= (2 * layer_range - 2)
    if i < layer_range:
        return i
    return 2 * layer_range - i - 2


def _get_all_scanner_locs(firewall_ranges: dict[int, int], i: int) -> dict[int, int]:
    scanner = {}
    for k, v in firewall_ranges.items():
        scanner[k] = _scanner_loc(v, i)
    return scanner


# def _will_get_caught(firewall_ranges: dict[int, int], delay: int) -> bool:
#     for i in range(max(firewall_ranges) + 1):
#         scanner = _get_all_scanner_locs(firewall_ranges, i + delay)
#         if scanner.get(i) == 0:
#             return True
#     return False


def solve_part_1(puzzle_input: list[str]):
    firewall_ranges = parse_input(puzzle_input)
    severity = 0
    for i in range(max(firewall_ranges) + 1):
        scanner = _get_all_scanner_locs(firewall_ranges, i)
        if scanner.get(i) == 0:
            severity += (i * firewall_ranges[i])
    return severity


def solve_part_2(puzzle_input: list[str]):
    firewall_ranges = parse_input(puzzle_input)

    # initial (naive) attempt
    # delay = 0
    # while _will_get_caught(firewall_ranges, delay):
    #     delay += 1
    # return delay

    # optimized solution
    MAX_DELAY_TO_CONSIDER = 10_000_000

    delay_valid = [True] * MAX_DELAY_TO_CONSIDER

    for depth, layer_range in firewall_ranges.items():
        for i in range(2 * layer_range - 2 - depth, MAX_DELAY_TO_CONSIDER, 2 * layer_range - 2):
            delay_valid[i] = False

    for i, is_valid in enumerate(delay_valid):
        if is_valid:
            return i

    return f"No solution with delay < {MAX_DELAY_TO_CONSIDER}"
