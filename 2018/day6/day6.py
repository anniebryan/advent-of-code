import re
from collections import defaultdict

coords = open('2018/day6/day6.txt').readlines()
points = [tuple(map(int, re.findall(r'\d+', x))) for x in coords]

# get min and max bounds
x_min = min(points, key = lambda a: a[0])[0]
x_max = max(points, key = lambda a: a[0])[0]
y_min = min(points, key = lambda a: a[1])[1]
y_max = max(points, key = lambda a: a[1])[1]
    
def manhattan(p1, p2):
    '''
    returns manhattan distance between p1 and p2
    '''
    p1_x, p1_y = p1
    p2_x, p2_y = p2
    return abs(p1_x - p2_x) + abs(p1_y - p2_y)


def distances(p1, points):
    '''
    returns distance from p to all points
    '''
    d = []
    for i, p2 in enumerate(points):
        dist = manhattan(p1, p2)
        d.append((dist, i))
    return sorted(d)


def part_1():
    closest = defaultdict(int)
    extend_to_inf = set()
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            d = distances((x, y), points)
            if d[0][0] != d[1][0]:
                closest[d[0][1]] += 1
                if x in [x_min, x_max] or y in [y_min, y_max]: # perimeter
                    extend_to_inf.add(d[0][1])

    for inf in extend_to_inf:
        closest.pop(inf)
        
    return max(closest.values())


def part_2():
    region = set()
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            dists = distances((x, y), points)
            total_d = sum([d[0] for d in dists])
            if total_d < 10000:
                region.add((x, y))
    return len(region)


print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))
