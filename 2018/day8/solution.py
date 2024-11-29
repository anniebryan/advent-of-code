import re

text = open('2018/day8/puzzle.txt').read()

def process_data(data):
    num_children = next(data)
    num_metadata = next(data)
    children = [process_data(data) for _ in range(num_children)]
    metadata = [next(data) for _ in range(num_metadata)]
    return children, metadata


def part_1():
    # returns sum of metadata values for all nodes
    def sum_metadata(node):
        children, metadata = node
        return sum(metadata) + sum(sum_metadata(child) for child in children)

    data = (int(d) for d in re.findall(r'\d+', text))
    root = process_data(data)
    return sum_metadata(root)


def part_2():
    # returns value of root node
    def value(node):
        children, metadata = node
        if not children:
            return sum(metadata)
        else:
            return sum([value(children[m-1]) for m in metadata if m <= len(children)])

    data = (int(d) for d in re.findall(r'\d+', text))
    root = process_data(data)
    return value(root)


print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))
