day = 9

example_filename = f'day{day}/day{day}_ex.txt'
example_input = [r.strip() for r in open(example_filename).readlines()]

example2_filename = f'day{day}/day{day}_ex2.txt'
example2_input = [r.strip() for r in open(example2_filename).readlines()]

filename = f'day{day}/day{day}.txt'
puzzle_input = [r.strip() for r in open(filename).readlines()]

def get_moves(input):
  moves = []
  for row in input:
    direction, num = row.split(" ")
    for _ in range(int(num)):
      moves.append(direction)
  return moves

def move_head(head, move):
  new_x = head[0] + {"R": 1, "L": -1, "U": 0, "D": 0}[move]
  new_y = head[1] + {"R": 0, "L": 0, "U": 1, "D": -1}[move]
  return (new_x, new_y)

def sign(n):
  return 0 if n == 0 else int(n/abs(n))
  
def move_tail(head, tail):
  head_x, head_y = head
  tail_x, tail_y = tail

  diff_x = head_x - tail_x
  diff_y = head_y - tail_y

  if -1 <= diff_x <= 1 and -1 <= diff_y <= 1:
    return tail # already touching, don't need to move
  return (tail_x + sign(diff_x), tail_y + sign(diff_y))

def execute_moves(moves, num_tails):
  head = (0, 0)
  tails = {i+1: (0, 0) for i in range(num_tails)}
  tail_locations = {tails[num_tails]}
  for move in moves:
    head = move_head(head, move)
    tails[1] = move_tail(head, tails[1])
    for i in range(1, num_tails):
      tails[i+1] = move_tail(tails[i], tails[i+1])
    tail_locations.add(tails[num_tails])
  return tail_locations

def part_1(input):
  moves = get_moves(input)
  return len(execute_moves(moves, 1))

def part_2(input):
  moves = get_moves(input)
  return len(execute_moves(moves, 9))


print(f'Part 1 example:        {part_1(example_input)}')
print(f'Part 1 puzzle:         {part_1(puzzle_input)}\n-')

print(f'Part 2 example:        {part_2(example_input)}')
print(f'Part 2 larger example: {part_2(example2_input)}')
print(f'Part 2 puzzle:         {part_2(puzzle_input)}')
