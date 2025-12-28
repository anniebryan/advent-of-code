"""
Advent of Code 2023
Day 22: Sand Slabs
"""

from collections import defaultdict, deque


def parse_input(puzzle_input: list[str], part_2: bool):
    bricks = []
    for line in puzzle_input:
        brick = set()
        coord_1, coord_2 = line.split("~")
        x1, y1, z1 = map(int, coord_1.split(","))
        x2, y2, z2 = map(int, coord_2.split(","))
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    brick.add((x, y, z))
        bricks.append(brick)
    return bricks


def drop_bricks(bricks: list[set[tuple[int, int, int]]]) -> list[set[tuple[int, int, int]]]:
    brick_map = {i: brick for i, brick in enumerate(bricks)}
    all_locs = {loc for brick in bricks for loc in brick}
    can_drop = True
    while can_drop:
        can_drop = False
        for i, brick in brick_map.items():
            shifted_brick = {(x, y, z - 1) for (x, y, z) in brick}
            if any(z <= 0 for (_, _, z) in shifted_brick):
                continue
            locs_to_check = shifted_brick - brick
            if not any(loc in all_locs for loc in locs_to_check):
                can_drop = True
                brick_map[i] = shifted_brick
                all_locs = all_locs - brick | shifted_brick
    return [brick_map[i] for i in sorted(brick_map)]


def determine_supports(bricks: list[set[tuple[int, int, int]]]) -> dict[int, set[int]]:
    supported_by = defaultdict(set)
    for l1, b1 in enumerate(bricks):
        for l2, b2 in enumerate(bricks):
            if l1 == l2:
                continue
            shifted_b1 = {(x, y, z - 1) for (x, y, z) in b1}
            if shifted_b1 & b2:
                supported_by[l1].add(l2)
    return supported_by


def solve_part_1(puzzle_input: list[str]):
    bricks = parse_input(puzzle_input, False)
    bricks = drop_bricks(bricks)

    supported_by = determine_supports(bricks)
    cannot_remove = {min(v) for v in supported_by.values() if len(v) == 1}

    return len(bricks) - len(cannot_remove)


def solve_part_2(puzzle_input: list[str]):
    bricks = parse_input(puzzle_input, True)
    bricks = drop_bricks(bricks)

    supported_by = determine_supports(bricks)
    cannot_remove = {min(v) for v in supported_by.values() if len(v) == 1}

    # inverse of supported_by
    supporting = defaultdict(set)
    for k, v in supported_by.items():
        for b in v:
            supporting[b].add(k)

    tot = 0
    for brick in cannot_remove:
        supported_by_copy = {k: set(v) for k, v in supported_by.items()}
        fallen = {brick}
        q = deque(list(supporting[brick]))
        while q:
            b = q.popleft()
            if b in fallen:
                continue
            supported_by_copy[b] -= fallen
            if not supported_by_copy[b]:
                fallen.add(b)
                q.extend(supporting[b])
        tot += len(fallen) - 1
    return tot
