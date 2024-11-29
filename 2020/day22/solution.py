from collections import deque

filename = '2020/day22/day22.txt'
puzzle_input = open(filename).read()

def get_initial_decks():
    player_1, player_2 = puzzle_input.split('\n\n')
    p1 = deque()
    for card in player_1.split('\n')[1:]:
        p1.append(int(card))
    p2 = deque()
    for card in player_2.split('\n')[1:]:
        p2.append(int(card))
    return p1, p2

def play_round(p1, p2):
    p1_card = p1.popleft()
    p2_card = p2.popleft()
    if p1_card > p2_card:
        p1.extend([p1_card, p2_card])
    else:
        p2.extend([p2_card, p1_card])
    return p1, p2

def to_str(p1, p2):
    return "".join(str(card) for card in p1) + "-" + "".join(str(card) for card in p2)

def get_new_deques(p1, p1_card, p2, p2_card):
    new_p1 = deque()
    for i in range(p1_card):
        new_p1.append(p1[i])
    new_p2 = deque()
    for i in range(p2_card):
        new_p2.append(p2[i])
    return new_p1, new_p2

def play_recursive_round(p1, p2, seen):
    if to_str(p1, p2) in seen:
        while p2:
            p1.append(p2.pop())
        return p1, p2, seen
    else:
        seen.add(to_str(p1, p2))
    p1_card = p1.popleft()
    p2_card = p2.popleft()
    if len(p1) >= p1_card and len(p2) >= p2_card:
        new_p1, new_p2 = get_new_deques(p1, p1_card, p2, p2_card)
        score_1, score_2 = play_recursive_game(new_p1, new_p2)
        if score_1 > score_2:
            p1.extend([p1_card, p2_card])
        else:
            p2.extend([p2_card, p1_card])
    else:
        if p1_card > p2_card:
            p1.extend([p1_card, p2_card])
        else:
            p2.extend([p2_card, p1_card])
    return p1, p2, seen

def score(queue):
    s, i = 0, 1
    while queue:
        s += i * queue.pop()
        i += 1
    return s

def play_game():
    p1, p2 = get_initial_decks()
    while len(p1) > 0 and len(p2) > 0:
        p1, p2 = play_round(p1, p2)
    return score(p1), score(p2)

def play_recursive_game(p1=None, p2=None):
    if p1 is None or p2 is None:
        p1, p2 = get_initial_decks()
    seen = set()
    while len(p1) > 0 and len(p2) > 0:
        p1, p2, seen = play_recursive_round(p1, p2, seen)
    return score(p1), score(p2)

def part_1():
    return max(play_game())

def part_2():
    return max(play_recursive_game())

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))