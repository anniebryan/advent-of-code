"""
Advent of Code 2018
Day 10: The Stars Align
"""

import regex as re


def get_data(puzzle_input):
    data = [[int(x) for x in re.findall(r'-?\d+', i)] for i in puzzle_input]
    return data


def get_boxes(data):
    boxes = []
    for i in range(20000):
        minx, maxx, miny, maxy = 10000, 0, 10000, 0
        for row in data:
            x, y, vx, vy = row
            newx = x + i * vx
            newy = y + i * vy
            
            minx = min(minx, newx)
            maxx = max(maxx, newx)
            miny = min(miny, newy)
            maxy = max(maxy, newy)
        boxes.append([maxx, minx, maxy, miny])
    return boxes


def get_box_size(box):
    maxx, minx, maxy, miny = box
    return maxx - minx + maxy - miny


def get_smallest_box(boxes):
    answer_box = min(get_box_size(box) for box in boxes)
    for i, box in enumerate(boxes):
        maxx, minx, maxy, miny = box
        if answer_box == maxx - minx + maxy - miny:
            return i, box


def solve_part_1(puzzle_input):
    data = get_data(puzzle_input)
    boxes = get_boxes(data)
    i, box = get_smallest_box(boxes)
    maxx, minx, maxy, miny = box

    grid = [[' '] * (maxx - minx + 1) for j in range(miny, maxy + 1)]
    for (x, y, vx, vy) in data:
        grid[y - miny + i * vy][x - minx + i * vx] = '#'

    output = ["\n"]
    for row in grid:
        output.append(" ".join(row))
    return "\n".join(output)


def solve_part_2(puzzle_input):
    data = get_data(puzzle_input)
    boxes = get_boxes(data)
    i, _ = get_smallest_box(boxes)
    return i
