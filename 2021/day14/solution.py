from collections import defaultdict, deque

day = 14

# example_filename = f'day{day}/day{day}_ex.txt'
# example_input = open(example_filename).readlines()
# template = example_input[0].strip()
# rules = [tuple(rule.strip().split(' -> ')) for rule in example_input[2:]]

filename = f'day{day}/day{day}.txt'
puzzle_input = open(filename).readlines()
template = puzzle_input[0].strip()
rules = [tuple(rule.strip().split(' -> ')) for rule in puzzle_input[2:]]


def execute_rules(text):
  new_text = deque()
  for rule in rules:
    pair, char = rule
    a_valid = False
    while text:
      while not a_valid:
        (a, a_valid) = text.popleft()
        new_text.append((a, a_valid))

      (b, b_valid) = text.popleft()
      while not b_valid:
        new_text.append((b, b_valid))
        (b, b_valid) = text.popleft()
      if f'{a}{b}' == pair:
        new_text.append((char, False))
      new_text.append((b, b_valid))
      (a, a_valid) = (b, b_valid)
    while new_text:
      text.append(new_text.popleft())
  return text

def n_steps(text, n):
  for _ in range(n):
    new_text = execute_rules(text)
    text = deque()
    while new_text:
      char, _ = new_text.popleft()
      text.append((char, True))
  return text

def difference(text):
  counts = defaultdict(int)
  for s in text:
    counts[s] += 1
  
  most_common = max(counts, key=counts.get)
  least_common = min(counts, key=counts.get)

  return counts[most_common] - counts[least_common]

def part_1():
  text = deque()
  for s in template:
    text.append((s, True))
  text = n_steps(text, 10)
  return difference(text)

def part_2():
  text = deque()
  for s in template:
    text.append((s, True))
  text = n_steps(text, 40)
  return difference(text)
  # code is too slow TODO

print(f'Part 1: {part_1()}')
print(f'Part 2: {part_2()}')
