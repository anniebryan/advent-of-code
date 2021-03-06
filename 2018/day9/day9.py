import re
from collections import deque, defaultdict

def get_info():
    text = open('2018/day9/day9.txt').read()
    pattern = r'([\d]+) players; last marble is worth ([\d]+) points'
    num_players, last_marble = map(lambda x: int(x), re.findall(pattern, text)[0])
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


def part_1():
    num_players, last_marble = get_info()
    return run_game(num_players, last_marble)


def part_2():
    num_players, last_marble = get_info()
    last_marble *= 100
    return run_game(num_players, last_marble)

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))
