import csv

file = open('2019/day3/puzzle.txt')
csv_reader = csv.reader(file, delimiter=',')
wire_1, wire_2 = [[(i[0], int(i[1:])) for i in row] for row in csv_reader]


def combine(loc, dir):
    change_by = {'L':(-1,0),
                 'R':(1,0),
                 'U':(0,1),
                 'D':(0,-1)}
    new_loc = tuple(loc[i] + change_by[dir[0]][i]*dir[1] for i in range(2))
    return new_loc


def get_vertices(wire, current_loc = (0,0)):
    if not wire: return [current_loc]
    new_loc = combine(current_loc, wire[0])
    return [current_loc] + get_vertices(wire[1:], new_loc)


def get_path(vertices):
    if len(vertices) < 2: return []
    if vertices[0][0] == vertices[1][0]:
        if vertices[0][1] < vertices[1][1]:
            path = [(vertices[0][0], i+1) for i in range(vertices[0][1], vertices[1][1])]
        else:
            path = [(vertices[0][0], i) for i in range(vertices[1][1], vertices[0][1])][::-1]
    else:
        if vertices[0][0] < vertices[1][0]:
            path = [(i+1, vertices[0][1]) for i in range(vertices[0][0], vertices[1][0])]
        else:
            path = [(i, vertices[0][1]) for i in range(vertices[1][0], vertices[0][0])][::-1]
    return path + get_path(vertices[1:])


def get_manhattan_distance(loc):
    return abs(loc[0])+abs(loc[1])


def get_intersections():
    path_1 = set(get_path(get_vertices(wire_1)))
    path_2 = set(get_path(get_vertices(wire_2)))
    intersections = path_1 & path_2
    return intersections


def part_1():
    distances = {get_manhattan_distance(i):i for i in get_intersections()}
    return min(distances)


def get_steps_so_far(path1, path2, loc):
    return path1.index(loc) + path2.index(loc) + 2


def part_2():
    v1 = get_path(get_vertices(wire_1))
    v2 = get_path(get_vertices(wire_2))
    steps_so_far = {get_steps_so_far(v1,v2,i):i for i in get_intersections()}
    return min(steps_so_far)


print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))
