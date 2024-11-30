from collections import defaultdict

def get_point_pairs(puzzle_input):
    point_pairs = []
    for line in puzzle_input:
        points = []
        for point in line.split(' -> '):
            points.append(tuple([int(val) for val in point.split(',')]))
        point_pairs.append(tuple(points))
    return point_pairs

def generate_diagram(puzzle_input, diagonals):
    point_pairs = get_point_pairs(puzzle_input)
    diagram = defaultdict(int)
    for point_pair in point_pairs:
        ((x1, y1), (x2, y2)) = point_pair
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        if x1 == x2: # horizontal
            for y in range(min_y, max_y + 1):
                diagram[(x1, y)] += 1
        elif y1 == y2: # vertical
            for x in range(min_x, max_x + 1):
                diagram[(x, y1)] += 1
        elif diagonals: # diagonal
            if (x1 == max_x and y1 == max_y) or (x2 == max_x and y2 == max_y):
                for i in range(max_x - min_x + 1):
                    diagram[(min_x + i, min_y + i)] += 1
            else:
                for i in range(max_x - min_x + 1):
                    diagram[(min_x + i, max_y - i)] += 1
    return diagram

def part_1(puzzle_input):
    diagram = generate_diagram(puzzle_input, False)
    return len([key for key in diagram if diagram[key] >= 2])

def part_2(puzzle_input):
    diagram = generate_diagram(puzzle_input, True)
    return len([key for key in diagram if diagram[key] >= 2])
