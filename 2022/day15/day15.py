import re
from collections import defaultdict

day = 15

example_filename = f'day{day}/day{day}_ex.txt'
example_input = [r.strip() for r in open(example_filename).readlines()]

filename = f'day{day}/day{day}.txt'
puzzle_input = [r.strip() for r in open(filename).readlines()]


def get_sensor_beacon_coordinates(input):
  int_regex = "(-?\d+)"
  for row in input:
    coordinates = re.match(f"Sensor at x={int_regex}, y={int_regex}: closest beacon is at x={int_regex}, y={int_regex}", row)
    (sensor_x, sensor_y, beacon_x, beacon_y) = map(int, coordinates.groups())
    yield (sensor_x, sensor_y, beacon_x, beacon_y)

def get_beacons(input):
  beacons = defaultdict(set)
  for (_, _, beacon_x, beacon_y) in get_sensor_beacon_coordinates(input):
    beacons[beacon_y].add(beacon_x)
  return beacons

def get_impossible_beacon_ranges(input, verbose=False):
  # maps row -> list of tuples (a, b) where a beacon cannot exist in any of the points (a, row)...(b-1, row)
  impossible_ranges = defaultdict(list)

  manhattan_distance = lambda x1, y1, x2, y2: abs(x1 - x2) + abs(y1 - y2)

  for i, (sensor_x, sensor_y, beacon_x, beacon_y) in enumerate(get_sensor_beacon_coordinates(input)):
    if verbose:
      print(f"Row {i+1}/{len(input)}")

    d = manhattan_distance(sensor_x, sensor_y, beacon_x, beacon_y)
    for y in range(-d, d + 1):
      row = sensor_y + y
      max_x = d - abs(y)
      impossible_ranges[row].append((sensor_x - max_x, sensor_x + max_x + 1))

  return impossible_ranges

def find_impossible_positions(input, row):
  impossible_ranges = get_impossible_beacon_ranges(input)[row]
  beacons = get_beacons(input)
  impossible_positions = set()

  for (a, b) in impossible_ranges:
    for i in range(a, b):
      if i not in beacons[row]:
        impossible_positions.add(i)

  return impossible_positions

def find_remaining_sensor(input, max_to_search):
  impossible_ranges = get_impossible_beacon_ranges(input)
  for i in range(max_to_search + 1):
    sorted_ranges = sorted(impossible_ranges[i], key=lambda r: r[0])
    max_found = sorted_ranges[0][1]
    for j in range(len(sorted_ranges) - 1):
      range_1 = sorted_ranges[j]
      range_2 = sorted_ranges[j+1]
      if range_2[0] > max_found:
        return (range_1[1], i)
      max_found = max(max_found, range_2[1])

def part_1(input, row):
  return len(find_impossible_positions(input, row))

def part_2(input, max_to_search):
  (x, y) = find_remaining_sensor(input, max_to_search)
  return x * 4000000 + y


print(f'Part 1 example: {part_1(example_input, 10)}')
print(f'Part 1 puzzle: {part_1(puzzle_input, 2000000)}')

print(f'Part 2 example: {part_2(example_input, 20)}')
print(f'Part 2 puzzle: {part_2(puzzle_input, 4000000)}')
