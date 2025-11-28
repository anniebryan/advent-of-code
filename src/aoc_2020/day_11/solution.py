"""
Advent of Code 2020
Day 11: Seating System
"""

def get_area_dimensions(puzzle_input):
    width = len(puzzle_input)
    height = len(puzzle_input[0])
    return width, height


def get_seat_locations(puzzle_input):
    width, height = get_area_dimensions(puzzle_input)
    seats = set()
    for i in range(width):
        for j in range(height):
            if puzzle_input[i][j] == 'L':
                seats.add((i, j))
    return seats


def get_visible_seats(puzzle_input, seats, i, j, adjacent):
    width, height = get_area_dimensions(puzzle_input)
    visible_seats = set()
    for d_i in {-1, 0, 1}:
        for d_j in {-1, 0, 1}:
            if d_i != 0 or d_j != 0:
                x = i + d_i
                y = j + d_j
                if not adjacent:
                    while 0 <= x < width and 0 <= y < height and (x, y) not in seats:
                        x += d_i
                        y += d_j
                if (x, y) in seats:
                    visible_seats.add((x, y))
    return visible_seats


def get_num_occupied(puzzle_input, seats, occupied, seat, adjacent):
    i, j = seat
    visible_seats = get_visible_seats(puzzle_input, seats, i, j, adjacent)
    n = 0
    for a in visible_seats:
        if a in occupied:
            n += 1
    return n


def timestep(puzzle_input, seats, occupied, adjacent, threshold):
    new_occupied = set()
    for seat in seats:
        if seat not in occupied:  # empty
            if get_num_occupied(puzzle_input, seats, occupied, seat, adjacent) == 0:
                new_occupied.add(seat)
        else:  # occupied
            if get_num_occupied(puzzle_input, seats, occupied, seat, adjacent) < threshold:
                new_occupied.add(seat)
    return new_occupied


def run_until_steady_state(puzzle_input, adjacent, threshold):
    seats = get_seat_locations(puzzle_input)
    occupied = set()
    new_occupied = timestep(puzzle_input, seats, occupied, adjacent, threshold)
    while occupied != new_occupied:
        occupied = new_occupied
        new_occupied = timestep(puzzle_input, seats, occupied, adjacent, threshold)
    return new_occupied


def solve_part_1(puzzle_input: list[str]):
    return len(run_until_steady_state(puzzle_input, True, 4))


def solve_part_2(puzzle_input: list[str]):
    return len(run_until_steady_state(puzzle_input, False, 5))
