"""
Advent of Code 2022
Day 2: Rock Paper Scissors
"""

def get_score(row, part_1):
    opp, me = row.split(" ")
    opp_move = {"A": 0, "B": 1, "C": 2}[opp]

    if part_1:
        move_score = {"X": 1, "Y": 2, "Z": 3}[me]
        outcome_score = 3 * ((move_score - opp_move) % 3)
    else:
        move_score = 1 + (opp_move + {"X": -1, "Y": 0, "Z": 1}[me]) % 3
        outcome_score = {"X": 0, "Y": 3, "Z": 6}[me]
    
    return move_score + outcome_score


def part_1(puzzle_input):
    return sum([get_score(row, True) for row in puzzle_input])


def part_2(puzzle_input):
    return sum([get_score(row, False) for row in puzzle_input])
