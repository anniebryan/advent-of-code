from collections import defaultdict

day = 8

example_filename = f'day{day}/day{day}_ex.txt'
example_input = open(example_filename).readlines()

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()

def get_lines(input):
  return [[[val.strip() for val in x.split(' ')] for x in line.split(' | ')] for line in input]

TOP = 'top'
TOP_LEFT = 'top left'
TOP_RIGHT = 'top right'
MIDDLE = 'middle'
BOTTOM_LEFT = 'bottom left'
BOTTOM_RIGHT = 'bottom right'
BOTTOM = 'bottom'

segments = {TOP, TOP_LEFT, TOP_RIGHT, MIDDLE, BOTTOM_LEFT, BOTTOM_RIGHT, BOTTOM}

nums = {
  0: {TOP, TOP_LEFT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT, BOTTOM},
  1: {TOP_RIGHT, BOTTOM_RIGHT},
  2: {TOP, TOP_RIGHT, MIDDLE, BOTTOM_LEFT, BOTTOM},
  3: {TOP, TOP_RIGHT, MIDDLE, BOTTOM_RIGHT, BOTTOM},
  4: {TOP_LEFT, TOP_RIGHT, MIDDLE, BOTTOM_RIGHT},
  5: {TOP, TOP_LEFT, MIDDLE, BOTTOM_RIGHT, BOTTOM},
  6: {TOP, TOP_LEFT, MIDDLE, BOTTOM_LEFT, BOTTOM_RIGHT, BOTTOM},
  7: {TOP, TOP_RIGHT, BOTTOM_RIGHT},
  8: {TOP, TOP_LEFT, TOP_RIGHT, MIDDLE, BOTTOM_LEFT, BOTTOM_RIGHT, BOTTOM},
  9: {TOP, TOP_LEFT, TOP_RIGHT, MIDDLE, BOTTOM_RIGHT, BOTTOM}
}

def get_count(letter_counts, loc):
  segment_counts = {segment: len(list(filter(lambda num: segment in nums[num], nums))) for segment in segments}
  return filter(lambda l: letter_counts[l] == segment_counts[loc], letter_counts).__next__()

def get_signal(signals, length):
  return [signal for signal in signals if len(signal) == length][0]

def get_output_number(line):
  signals, output = line
  letter_counts = defaultdict(int)
  for signal in signals:
    for letter in signal:
      letter_counts[letter] += 1
  
  top_left = get_count(letter_counts, TOP_LEFT)
  bottom_left = get_count(letter_counts, BOTTOM_LEFT)
  bottom_right = get_count(letter_counts, BOTTOM_RIGHT)
  top_right = filter(lambda l: l != bottom_right, get_signal(signals, len(nums[1]))).__next__()
  top = filter(lambda l: l not in {top_right, bottom_right}, get_signal(signals, len(nums[7]))).__next__()
  middle = filter(lambda l: l not in {top_left, top_right, bottom_right}, get_signal(signals, len(nums[4]))).__next__()
  bottom = filter(lambda l: l not in {top_left, bottom_left, bottom_right, top_right, top, middle}, letter_counts).__next__()
  
  mapping = {
    top: TOP,
    top_left: TOP_LEFT,
    top_right: TOP_RIGHT,
    middle: MIDDLE,
    bottom_left: BOTTOM_LEFT,
    bottom_right: BOTTOM_RIGHT,
    bottom: BOTTOM
  }
  
  return int(''.join([str(filter(lambda n: nums[n] == {mapping[letter] for letter in val}, nums).__next__()) for val in output]))

def part_1(input):
  lines = get_lines(input)
  return sum([sum([1*(len(item) in {2,3,4,7}) for item in line[1]]) for line in lines])

def part_2(input):
  lines = get_lines(input)
  return sum(list(map(get_output_number, lines)))


print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
