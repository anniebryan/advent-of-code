"""
Advent of Code 2018
Day 9: Marble Mania
"""

import re
from collections import deque, defaultdict

def get_info(puzzle_input):
    pattern = r'([\d]+) players; last marble is worth ([\d]+) points'
    num_players, last_marble = map(lambda x: int(x), re.findall(pattern, puzzle_input[0])[0])
    return num_players, last_marble

def take_turn(current_marble_index, marble_to_place, player, circle, scores):
    if marble_to_place % 23 == 0:
        scores[player] += marble_to_place
        index_to_remove = (current_marble_index - 7)%len(circle)
        scores[player] += circle[index_to_remove]
        new_circle = circle[:index_to_remove] + circle[index_to_remove+1:]
        new_current_marble_index = index_to_remove
    else:
        index_to_add = (current_marble_index + 2)%len(circle)
        new_circle = circle[:index_to_add] + [marble_to_place] + circle[index_to_add:]
        new_current_marble_index = index_to_add
    return new_current_marble_index, new_circle, scores


def run_game(num_players, last_marble):
    scores = defaultdict(int)
    circle = deque([0])

    for marble in range(last_marble):
        if (marble+1)%23 == 0:
            circle.rotate(7)
            index_to_remove = (marble+1)%num_players
            scores[index_to_remove] += marble + 1 + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble+1)

    return max(scores.values())


def part_1(puzzle_input):
    num_players, last_marble = get_info(puzzle_input)
    return run_game(num_players, last_marble)


def part_2(puzzle_input):
    num_players, last_marble = get_info(puzzle_input)
    last_marble *= 100
    return run_game(num_players, last_marble)
