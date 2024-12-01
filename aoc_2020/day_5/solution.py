"""
Advent of Code 2020
Day 5: Binary Boarding
"""

def binary_search(s, low_c, high_val):
    low, high = 0, high_val
    for c in s:
        mid = int((low + high) / 2)
        if c == low_c:  # lower half
            high = mid
        else:  # upper half
            low = mid + 1
    return low


def get_seat_id(boarding_pass):
    row = binary_search(boarding_pass[:7], 'F', 127)
    col = binary_search(boarding_pass[7:10], 'L', 7)
    return 8 * row + col


def highest_seat_id(puzzle_input):
    highest = 0
    for boarding_pass in puzzle_input:
        seat_id = get_seat_id(boarding_pass)
        highest = max(highest, seat_id)
    return highest


def all_seat_ids(puzzle_input):
    ids = set()
    for boarding_pass in puzzle_input:
        seat_id = get_seat_id(boarding_pass)
        ids.add(seat_id)
    return sorted(list(ids))


def find_missing_id(puzzle_input):
    ids = all_seat_ids(puzzle_input)
    i, j = 0, len(ids) - 1
    while j > i + 1:
        mid = int((i + j) / 2)
        if ids[i] - i != ids[mid] - mid:
            j = mid
        else:
            i = mid
    return ids[j] - 1


def solve_part_1(puzzle_input):
    return highest_seat_id(puzzle_input)


def solve_part_2(puzzle_input):
    return find_missing_id(puzzle_input)
