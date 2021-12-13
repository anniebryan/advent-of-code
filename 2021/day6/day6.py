from collections import defaultdict

day = 6

# example_filename = f'day{day}/day{day}_ex.txt'
# example_input = open(example_filename).readlines()
# initial_timers = [int(val) for val in example_input[0].split(',')]

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()
initial_timers = [int(val) for val in puzzle_input[0].split(',')]

def simulate_day(timers):
  new_timers = {key-1: val for key, val in timers.items() if key != 0}
  if 0 in timers:
    new_timers[6] = new_timers[6] + timers[0] if 6 in new_timers else timers[0]
    new_timers[8] = new_timers[8] + timers[0] if 8 in new_timers else timers[0]
  return new_timers
  
def simulate_n_days(timers, n):
  for _ in range(n):
    timers = simulate_day(timers)
  return timers

timers = defaultdict(int)
for val in initial_timers:
  timers[val] += 1

def part_1():
  return sum(simulate_n_days(timers, 80).values())

def part_2():
  return sum(simulate_n_days(timers, 256).values())

print(f'Part 1: {part_1()}')
print(f'Part 2: {part_2()}')
