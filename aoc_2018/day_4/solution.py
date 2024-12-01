"""
Advent of Code 2018
Day 4: Repose Record
"""

import regex as re
from collections import defaultdict


def parse_records(puzzle_input):
    pattern = r'\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.+)'
    records = [re.match(pattern, row).groups() for row in puzzle_input]

    total_minutes = defaultdict(int)  # maps guard ID --> total minutes asleep
    ind_minutes = defaultdict(lambda: defaultdict(int))  # maps guard ID --> minute --> instances asleep

    for line in sorted(records):
        if 'Guard' in line[5]:
            guard_id = int(re.findall(r'\d+', line[5])[0])
        elif 'asleep' in line[5]:
            min_0 = int(line[4])
        elif 'wakes' in line[5]:
            min_1 = int(line[4])
            total_minutes[guard_id] += min_1 - min_0
            for m in range(min_0, min_1):
                ind_minutes[guard_id][m] += 1

    return total_minutes, ind_minutes


def part_1(puzzle_input):
    total_minutes, ind_minutes = parse_records(puzzle_input)
    max_guard = max(total_minutes, key = total_minutes.get)  # guard who sleeps the most
    max_minute = max(ind_minutes[max_guard], key = ind_minutes[max_guard].get)
    return f"{max_guard} * {max_minute} = {max_guard * max_minute}"


def part_2(puzzle_input):
    _, ind_minutes = parse_records(puzzle_input)
    common_minutes = {}
    for guard in ind_minutes:
        most_common_minute = max(ind_minutes[guard], key = ind_minutes[guard].get)
        time_at_minute = ind_minutes[guard][most_common_minute]  # number of times guard was asleep during that minute
        common_minutes[guard] = (most_common_minute, time_at_minute)
    final_guard = max(common_minutes, key = lambda x: common_minutes[x][1])
    final_minute = common_minutes[final_guard][0]
    return f"{final_guard} * {final_minute} = {final_guard * final_minute}"
