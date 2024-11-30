"""
Advent of Code 2021
Day 8: Seven Segment Search
"""

from collections import defaultdict

TOP = 'top'
TOP_LEFT = 'top left'
TOP_RIGHT = 'top right'
MIDDLE = 'middle'
BOTTOM_LEFT = 'bottom left'
BOTTOM_RIGHT = 'bottom right'
BOTTOM = 'bottom'

SEGMENTS = {TOP, TOP_LEFT, TOP_RIGHT, MIDDLE, BOTTOM_LEFT, BOTTOM_RIGHT, BOTTOM}

NUMS = {
    0: {TOP, TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT, BOTTOM},
    1: {TOP_RIGHT, BOTTOM_RIGHT},
    2: {TOP, TOP_RIGHT, MIDDLE, BOTTOM_LEFT, BOTTOM},
    3: {TOP, TOP_RIGHT, MIDDLE, BOTTOM_RIGHT, BOTTOM},
    4: {TOP_LEFT, TOP_RIGHT, MIDDLE, BOTTOM_RIGHT},
    5: {TOP, TOP_LEFT, MIDDLE, BOTTOM_RIGHT, BOTTOM},
    6: {TOP, TOP_LEFT, MIDDLE, BOTTOM_LEFT, BOTTOM_RIGHT, BOTTOM},
    7: {TOP, TOP_RIGHT, BOTTOM_RIGHT},
    8: {TOP, TOP_LEFT, TOP_RIGHT, MIDDLE, BOTTOM_LEFT, BOTTOM_RIGHT, BOTTOM},
    9: {TOP, TOP_LEFT, TOP_RIGHT, MIDDLE, BOTTOM_RIGHT, BOTTOM}
}


def get_lines(puzzle_input):
    return [[[val.strip() for val in x.split(' ')] for x in line.split(' | ')] for line in puzzle_input]


def get_count(letter_counts, loc):
    segment_counts = {segment: len(list(filter(lambda num: segment in NUMS[num], NUMS))) for segment in SEGMENTS}
    return filter(lambda l: letter_counts[l] == segment_counts[loc], letter_counts).__next__()


def get_signal(signals, length):
    return [signal for signal in signals if len(signal) == length][0]


def get_output_number(line):
    signals, output = line
    letter_counts = defaultdict(int)
    for signal in signals:
        for letter in signal:
            letter_counts[letter] += 1
    
    top_left = get_count(letter_counts, TOP_LEFT)
    bottom_left = get_count(letter_counts, BOTTOM_LEFT)
    bottom_right = get_count(letter_counts, BOTTOM_RIGHT)
    top_right = filter(lambda l: l != bottom_right, get_signal(signals, len(NUMS[1]))).__next__()
    top = filter(lambda l: l not in {top_right, bottom_right}, get_signal(signals, len(NUMS[7]))).__next__()
    middle = filter(lambda l: l not in {top_left, top_right, bottom_right}, get_signal(signals, len(NUMS[4]))).__next__()
    bottom = filter(lambda l: l not in {top_left, bottom_left, bottom_right, top_right, top, middle}, letter_counts).__next__()
    
    mapping = {
        top: TOP,
        top_left: TOP_LEFT,
        top_right: TOP_RIGHT,
        middle: MIDDLE,
        bottom_left: BOTTOM_LEFT,
        bottom_right: BOTTOM_RIGHT,
        bottom: BOTTOM
    }
    
    return int(''.join([str(filter(lambda n: NUMS[n] == {mapping[letter] for letter in val}, NUMS).__next__()) for val in output]))


def part_1(puzzle_input):
    lines = get_lines(puzzle_input)
    return sum([sum([1 * (len(item) in {2, 3, 4, 7}) for item in line[1]]) for line in lines])


def part_2(puzzle_input):
    lines = get_lines(puzzle_input)
    return sum(list(map(get_output_number, lines)))
