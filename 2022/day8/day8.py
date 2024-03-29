day = 8

example_filename = f'day{day}/day{day}_ex.txt'
example_input = [r.strip() for r in open(example_filename).readlines()]

filename = f'day{day}/day{day}.txt'
puzzle_input = [r.strip() for r in open(filename).readlines()]

class Forest:
  def __init__(self, grid):
    self.height = len(grid)
    self.width = len(grid[0])
    self.trees = {}
    for i in range(self.height):
      self.trees[i] = {}
      for j in range(self.width):
        self.trees[i][j] = int(grid[i][j])

  def trees_to_edge(self, i, j):
    top = [self.trees[x][j] for x in range(i)][::-1]
    bottom = [self.trees[x][j] for x in range(i + 1, self.height)]
    left = [self.trees[i][y] for y in range(j)][::-1]
    right = [self.trees[i][y] for y in range(j + 1, self.width)]
    return (top, bottom, left, right)

  def is_visible(self, i, j):
    tree_height = self.trees[i][j]
    for dir in self.trees_to_edge(i, j):
      if len(dir) == 0 or tree_height > max(dir):
        return True
    return False

  def scenic_score(self, i, j):
    score = 1
    for dir in self.trees_to_edge(i, j):
      num_visible = 0
      for tree in dir:
        num_visible += 1
        if tree >= self.trees[i][j]:
          break
      score *= num_visible
    return score

def part_1(input):
  forest = Forest(input)
  visible_trees = 0
  for i in range(forest.height):
    for j in range(forest.width):
      if forest.is_visible(i, j):
        visible_trees += 1
  return visible_trees

def part_2(input):
  forest = Forest(input)
  max_scenic_score = 0
  for i in range(forest.height):
    for j in range(forest.width):
      max_scenic_score = max(max_scenic_score, forest.scenic_score(i, j))
  return max_scenic_score


print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
