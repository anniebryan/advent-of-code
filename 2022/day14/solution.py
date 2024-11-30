def points(line):
    path = []
    for point in line.split(' -> '):
        x, y = point.split(',')
        path.append((int(x), int(y)))

    start_point = path[0]
    for point in path[1:]:
        x, y = start_point
        if x == point[0]:
            for j in range(min(y, point[1]), max(y, point[1]) + 1):
                yield (x, j)
        if y == point[1]:
            for i in range(min(x, point[0]), max(x, point[0]) + 1):
                yield (i, y)
        start_point = point

def get_rock(input):
    rock = set()
    for line in input:
        for point in points(line):
            rock.add(point)
    xs = {p[0] for p in rock}
    ys = {p[1] for p in rock}
    x_range = (min(xs), max(xs))
    y_range = (min(ys), max(ys))
    return rock, x_range, y_range


def move(sand_loc, rock, sand):
    x, y = sand_loc
    filled = rock.union(sand)

    down = (x, y + 1)
    if down not in filled:
        return down

    diag_left = (x - 1, y + 1)
    if diag_left not in filled:
        return diag_left

    diag_right = (x + 1, y + 1)
    if diag_right not in filled:
        return diag_right
    
    # can't move
    return sand_loc


def print_pile(rock, sand):
    filled = rock.union(sand)
    xs = {p[0] for p in filled}
    ys = {p[1] for p in filled}
    s = ""
    for y in range(min(ys), max(ys)+1):
        for x in range(min(xs), max(xs)+1):
            if (x, y) in rock:
                s += "#"
            elif (x, y) in sand:
                s += "o"
            else:
                s += "."
        s += "\n"
    print(s)


def pour_sand(rock, y_max, sand_start, verbose=False):
    num_sand_dropped = 0
    sand = set()
    done = False
    while not done:
        if num_sand_dropped % 1000 == 0 and verbose:
            print_pile(rock, sand)

        # drop sand
        (prev_sand_loc, sand_loc) = (sand_start, move(sand_start, rock, sand))
        while prev_sand_loc != sand_loc and sand_loc[1] <= y_max:
            (prev_sand_loc, sand_loc) = (sand_loc, move(sand_loc, rock, sand))

        if sand_loc[1] > y_max:
            done = True
        else:
            num_sand_dropped += 1
        if sand_loc == sand_start:
            done = True

        sand.add(sand_loc)
    return num_sand_dropped
        

def part_1(input):
    rock, _, y_range = get_rock(input)
    y_max = y_range[1]
    return pour_sand(rock, y_max, (500, 0))

def part_2(input):  # TODO speedup
    rock, x_range, y_range = get_rock(input)
    x_min, x_max = x_range
    y_min, y_max = y_range

    floor_depth = y_max+2
    floor = points(f"{500-floor_depth-2},{floor_depth} -> {500+floor_depth+2},{floor_depth}")
    for point in floor:
        rock.add(point)
    return pour_sand(rock, floor_depth, (500, 0))
