from collections import defaultdict

filename = '2020/day13/day13.txt'
puzzle_input = open(filename).readlines()

def get_earliest_bus():
    return int(puzzle_input[0])

def get_bus_times():
    times = puzzle_input[1].split(',')
    return {int(x) for x in times if x != 'x'}

def next_bus_time():
    earliest_bus = get_earliest_bus()
    bus_times = get_bus_times()
    time_to_wait = {x: x - earliest_bus % x for x in bus_times}
    soonest_bus = min(time_to_wait, key = time_to_wait.get)
    return soonest_bus, time_to_wait[soonest_bus]

def get_departure_requirements():
    times = puzzle_input[1].split(',')
    return {(i, int(times[i])) for i in range(len(times)) if times[i] != 'x'}

def get_earliest_timestamp():
    requirements = get_departure_requirements()
    offsets = {(i[0] % i[1], i[1]) for i in requirements}
    time, inc = 0, 1
    for t, bus in offsets:
        if t > 0:
            val = bus - t
        else:
            val = 0
        while time % bus != val:
            time += inc
        inc *= bus
    return time

def part_1():
    output = next_bus_time()
    return output[0]*output[1]

def part_2():
    return get_earliest_timestamp()

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))