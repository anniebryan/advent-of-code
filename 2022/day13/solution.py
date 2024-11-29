import ast
from functools import cmp_to_key

day = 13

example_filename = f'day{day}/day{day}_ex.txt'
example_input = [r.strip() for r in open(example_filename).readlines()]

filename = f'day{day}/day{day}.txt'
puzzle_input = [r.strip() for r in open(filename).readlines()]

def compare_pair(left, right):
  """
  Inputs:
    left = a list containing 0 or more integers or other lists
    right = a list containing 0 or more integers or other lists
  Returns:
   -1 if left and right are in the "correct order" (left < right)
    1 if left and right are "out of order"         (left > right)
    0 if left and right are equivalent             (left = right)
  """
  # base case: one or both lists are empty
  if len(left) == 0:
    return 0 if len(right) == 0 else -1
  if len(left) > 0 and len(right) == 0:
    return 1

  left_val = left[0]
  right_val = right[0]

  if isinstance(left_val, int) and isinstance(right_val, int):
    if left_val == right_val:
      return compare_pair(left[1:], right[1:])
    return -1 if left_val < right_val else 1

  if isinstance(left_val, int):
    left_val = [left_val]

  if isinstance(right_val, int):
    right_val = [right_val]

  list_result = compare_pair(left_val, right_val)
  if list_result in {-1, 1}:
    return list_result
  return compare_pair(left[1:], right[1:])

def part_1(input):
  pairs = [(ast.literal_eval(input[i]), ast.literal_eval(input[i+1])) for i in range(0, len(input), 3)]
  in_order_idx_sum = 0
  for i, pair in enumerate(pairs):
    left, right = pair
    if compare_pair(left, right) == -1:
      in_order_idx_sum += i + 1
  return in_order_idx_sum

def part_2(input):
  packets = [ast.literal_eval(line) for line in input if len(line) > 0]
  divider_packets = ([[2]], [[6]])
  for packet in divider_packets:
    packets.append(packet)

  div_packet_idx_prod = 1
  for i, packet in enumerate(sorted(packets, key=cmp_to_key(compare_pair))):
    if packet in divider_packets:
      div_packet_idx_prod *= (i + 1)
  return div_packet_idx_prod

print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
