from itertools import cycle

############################
# Advent of Code 2022 Day 17
############################

def get_rocks():
    # in a function rather than a constant so that cycle resets after each call
    return cycle([
        [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 2, 'y': 0}, {'x': 3, 'y': 0}],
        [{'x': 1, 'y': 0}, {'x': 0, 'y': 1}, {'x': 1, 'y': 1}, {'x': 2, 'y': 1}, {'x': 1, 'y': 2}],
        [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 2, 'y': 0}, {'x': 2, 'y': 1}, {'x': 2, 'y': 2}],
        [{'x': 0, 'y': 0}, {'x': 0, 'y': 1}, {'x': 0, 'y': 2}, {'x': 0, 'y': 3}],
        [{'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 0, 'y': 1}, {'x': 1, 'y': 1}]
    ])


def can_move_horizontal(rock: list[dict], dx: int, ground: set[tuple]):
    for d in rock:
        x, y = d['x'], d['y']
        if not(0 <= x + dx <= 6):
            return False
        if (x + dx, y) in ground:
            return False
    return True


def can_drop(rock: list[dict], ground: set[tuple]):
    for d in rock:
        x, y = d['x'], d['y']
        if (x, y - 1) in ground:
            return False
    return True


def drop(rock: list[dict], ground: set[tuple], jet_queue: cycle):
    while True:
        j = jet_queue.__next__()
        dx = {"<": -1, ">": 1}[j]
        if can_move_horizontal(rock, dx, ground):
            for d in rock:
                d['x'] += dx
        if can_drop(rock, ground):
            for d in rock:
                d['y'] -= 1
        else:
            break


def update_cycles(history: dict[int, int], i: int, cycles: dict[int, tuple[int, int]]):
    for c in range(i):
        cycle_len = c + 1
        if i % cycle_len == 0:
            diff = history[i] - history[i - cycle_len]
            if cycle_len not in cycles:
                cycles[cycle_len] = (diff, 1)
            else:
                (d, n) = cycles[cycle_len]
                if d == diff:
                    cycles[cycle_len] = (d, n + 1)
                    # need to see same difference for 10 cycles
                    if n >= 9:
                        return (cycle_len, d)
                else:
                    cycles[cycle_len] = (diff, 1)
    return (None, None)


def drop_n_rocks(jet_queue, n):
    rocks = get_rocks()
    height = 0
    ground = set([(i, 0) for i in range(7)])
    history, cycles = {}, {}
    cycle_len, d, return_idx = None, None, None

    for i in range(n):
        if i == return_idx:
            return int(height + ((n - i) / cycle_len) * d)

        rock = [{'x': d['x'] + 2, 'y': d['y'] + height + 4} for d in rocks.__next__()]
        drop(rock, ground, jet_queue)
        ground.update((d['x'], d['y']) for d in rock)
        height = max(height, max(d['y'] for d in rock))

        if return_idx is None:
            history[i] = height
            (cycle_len, d) = update_cycles(history, i, cycles)
            if cycle_len is not None:
                return_idx = i + (n % cycle_len)

    return height


def part_1(puzzle_input):
    jet_queue = cycle(puzzle_input[0])
    return drop_n_rocks(jet_queue, 2022)

def part_2(puzzle_input):
    jet_queue = cycle(puzzle_input[0])
    return drop_n_rocks(jet_queue, 1000000000000)
