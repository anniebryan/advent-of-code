"""
Advent of Code 2022
Day 9: Rope Bridge
"""

def get_moves(puzzle_input):
    moves = []
    for row in puzzle_input:
        direction, num = row.split(" ")
        for _ in range(int(num)):
            moves.append(direction)
    return moves

def move_head(head, move):
    new_x = head[0] + {"R": 1, "L": -1, "U": 0, "D": 0}[move]
    new_y = head[1] + {"R": 0, "L": 0, "U": 1, "D": -1}[move]
    return (new_x, new_y)

def sign(n):
    return 0 if n == 0 else int(n/abs(n))
    
def move_tail(head, tail):
    head_x, head_y = head
    tail_x, tail_y = tail

    diff_x = head_x - tail_x
    diff_y = head_y - tail_y

    if -1 <= diff_x <= 1 and -1 <= diff_y <= 1:
        return tail # already touching, don't need to move
    return (tail_x + sign(diff_x), tail_y + sign(diff_y))

def execute_moves(moves, num_tails):
    head = (0, 0)
    tails = {i+1: (0, 0) for i in range(num_tails)}
    tail_locations = {tails[num_tails]}
    for move in moves:
        head = move_head(head, move)
        tails[1] = move_tail(head, tails[1])
        for i in range(1, num_tails):
            tails[i+1] = move_tail(tails[i], tails[i+1])
        tail_locations.add(tails[num_tails])
    return tail_locations

def part_1(puzzle_input):
    moves = get_moves(puzzle_input)
    return len(execute_moves(moves, 1))

def part_2(puzzle_input):
    moves = get_moves(puzzle_input)
    return len(execute_moves(moves, 9))
