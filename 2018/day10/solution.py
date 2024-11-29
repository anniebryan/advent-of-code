from re import findall

text = open('2018/day10/puzzle.txt').readlines()
data = [[int(x) for x in findall(r'-?\d+', i)] for i in text]

def get_boxes():
    boxes = []
    for i in range(20000):
        minx, maxx, miny, maxy = 10000, 0, 10000, 0
        for row in data:
            x, y, vx, vy = row
            newx = x + i*vx
            newy = y + i*vy
            
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

def part_1():
    boxes = get_boxes()
    i, box = get_smallest_box(boxes)
    maxx, minx, maxy, miny = box

    grid = [[' ']*(maxx - minx + 1) for j in range(miny, maxy + 1)]
    for (x, y, vx, vy) in data:
        grid[y - miny + i*vy][x - minx + i*vx] = '#'

    output = "\n"
    for row in grid:
        output += ' '.join(row)
        output += '\n'

    return output


def part_2():
    boxes = get_boxes()
    i, _ = get_smallest_box(boxes)
    return i


print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))
