from collections import defaultdict

day = 6

example_filename = f'day{day}/day{day}_ex.txt'
example_input = open(example_filename).readlines()

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()

def get_initial_timers(input):
  timers = defaultdict(int)
  for val in input[0].split(','):
    timers[int(val)] += 1
  return timers

def simulate_day(timers):
  new_timers = {key-1: val for key, val in timers.items() if key != 0}
  if 0 in timers:
    new_timers[6] = new_timers[6] + timers[0] if 6 in new_timers else timers[0]
    new_timers[8] = new_timers[8] + timers[0] if 8 in new_timers else timers[0]
  return new_timers
  
def simulate_n_days(input, n):
  timers = get_initial_timers(input)
  for _ in range(n):
    timers = simulate_day(timers)
  return timers

def part_1(input):
  return sum(simulate_n_days(input, 80).values())

def part_2(input):
  initial_timers = get_initial_timers(input)
  return sum(simulate_n_days(input, 256).values())


print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
