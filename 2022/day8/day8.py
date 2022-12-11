day = 8

example_filename = f'day{day}/day{day}_ex.txt'
example_input = [r.strip() for r in open(example_filename).readlines()]

filename = f'day{day}/day{day}.txt'
puzzle_input = [r.strip() for r in open(filename).readlines()]

class Forest:
  def __init__(self, grid):
    self.height = len(grid)
    self.width = len(grid[0])
    trees = {}
    for i in range(self.height): # rows
      row = grid[i]
      trees[i] = {}
      for j in range(self.width): # cols
        trees[i][j] = int(row[j])
    self.trees = trees

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

  def num_visible(self, dir, i, j):
    if len(dir) in {0, 1}:
      return len(dir)
    cant_see_below = dir[0]
    num_visible = 1
    for tree in dir[1:]:
      if tree >= self.trees[i][j]:
        return num_visible + 1
      if tree >= cant_see_below:
        num_visible += 1
        cant_see_below = tree
    return num_visible

  def scenic_score(self, i, j):
    score = 1
    for dir in self.trees_to_edge(i, j):
      score *= self.num_visible(dir, i, j)
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
      # TODO returning incorrect answer
      max_scenic_score = max(max_scenic_score, forest.scenic_score(i, j))
  return max_scenic_score


print(f'Part 1 example: {part_1(example_input)}')
print(f'Part 1 puzzle: {part_1(puzzle_input)}')

print(f'Part 2 example: {part_2(example_input)}')
print(f'Part 2 puzzle: {part_2(puzzle_input)}')
