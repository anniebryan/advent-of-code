"""
Advent of Code 2021
Day 4: Giant Squid
"""

def get_input_numbers(puzzle_input):
    return [int(n) for n in puzzle_input[0].split(',')]

def get_input_boards(puzzle_input):
    boards = []
    current_board = []
    for row in puzzle_input[2:]:
        if row == "":
            boards.append(current_board)
            current_board = []
        else:
            current_board.append([int(item) for item in row.split() if len(item) > 0])
    boards.append(current_board)

    boards_dict = {}
    for i, board in enumerate(boards):
        board_dict = {}
        for j, row in enumerate(board):
            for k, val in enumerate(row):
                board_dict[val] = (j, k)
        boards_dict[i] = board_dict
    return boards_dict

size = 5
row = lambda marked: any([all([(i, j) in marked for j in range(size)]) for i in range(size)])
col = lambda marked: any([all([(i, j) in marked for i in range(size)]) for j in range(size)])
wins = lambda marked: row(marked) or col(marked)

def part_1(puzzle_input):
    input_numbers = get_input_numbers(puzzle_input)
    input_boards = get_input_boards(puzzle_input)
    num_boards = len(input_boards)

    marked_spaces = {i: set() for i in range(num_boards)}
    for num in input_numbers:
        for j in range(num_boards):
            if num in input_boards[j]:
                marked_spaces[j].add(input_boards[j][num])
        has_won = [wins(marked_spaces[i]) for i in range(num_boards)]
        if any(has_won):
            winning_board_num = list(filter(lambda tup: tup[1], [(i, board) for i, board in enumerate(has_won)]))[0][0]
            winning_board = {input_boards[winning_board_num][n]: n for n in input_boards[winning_board_num]}
            all_spaces = {(i,j) for i in range(size) for j in range(size)}
            unmarked = [winning_board[s] for s in all_spaces if s not in marked_spaces[winning_board_num]]
            return sum(unmarked) * num

def part_2(puzzle_input):
    input_numbers = get_input_numbers(puzzle_input)
    input_boards = get_input_boards(puzzle_input)
    num_boards = len(input_boards)
    
    marked_spaces = {i: set() for i in range(num_boards)}
    prev_has_won = [wins(marked_spaces[i]) for i in range(num_boards)]
    for num in input_numbers:
        for j in range(num_boards):
            if num in input_boards[j]:
                marked_spaces[j].add(input_boards[j][num])
        has_won = [wins(marked_spaces[i]) for i in range(num_boards)]
        if all(has_won) and not all(prev_has_won):
            winning_board_num = list(filter(lambda tup: not tup[1], [(i, board) for i, board in enumerate(prev_has_won)]))[0][0]
            winning_board = {input_boards[winning_board_num][n]: n for n in input_boards[winning_board_num]}
            all_spaces = {(i,j) for i in range(size) for j in range(size)}
            unmarked = [winning_board[s] for s in all_spaces if s not in marked_spaces[winning_board_num]]
            return sum(unmarked) * num
        else:
            prev_has_won = has_won
