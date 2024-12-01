"""
Advent of Code 2022
Day 20: Grove Positioning System
"""

class Node:
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

    def link(self, node):
        self.next = node
        node.prev = self


class LinkedList:
    def __init__(self, decryption_key):
        self.nodes = []
        self.length = 0
        self.first_node = None
        self.last_node = None
        self.zero_node = None
        self.decryption_key = decryption_key

    def add_node(self, val):
        node = Node(val * self.decryption_key)

        if self.first_node is None:
            self.first_node = node
            self.last_node = node

        if val == 0:
            self.zero_node = node

        node.link(self.first_node)
        self.last_node.link(node)

        self.last_node = node
        self.nodes.append(node)
        self.length += 1

    def move_node(self, node):
        num_spaces = node.val % (self.length - 1)
        if num_spaces != 0:
            p = node
            for _ in range(num_spaces):
                p = p.next
            node.prev.link(node.next)
            n = p.next
            p.link(node)
            node.link(n)

    def num_after_zero(self, num):
        i = num % self.length
        node = self.zero_node
        for _ in range(i):
            node = node.next
        return node.val


def parse(puzzle_input, decryption_key):
    ls = LinkedList(decryption_key)
    for row in puzzle_input:
        ls.add_node(int(row))
    return ls


def solve(puzzle_input, decryption_key, num_times):
    ls = parse(puzzle_input, decryption_key)
    nodes = ls.nodes
    for _ in range(num_times):
        for node in nodes:
            ls.move_node(node)
    return sum([ls.num_after_zero(i) for i in [1000, 2000, 3000]])


def solve_part_1(puzzle_input):
    return solve(puzzle_input, 1, 1)


def solve_part_2(puzzle_input):
    return solve(puzzle_input, 811589153, 10)
