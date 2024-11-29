import string
from functools import reduce

s = open('2018/day5/puzzle.txt').read()

def destroy(p, c):
    # p: previous
    # c: current
    if p == None or len(p) == 0:
        return c
    else:
        l = str(p[-1:]) # last letter
        lc = string.ascii_lowercase
        uc = string.ascii_uppercase
        if (l in lc and c in uc) or (l in uc and c in lc): # opposite case
            if l.lower() == c.lower():
                return p[:-1]
        return p + c


def part_1():
    s2 = reduce(destroy, s)
    return len(s2)


def part_2():
    lengths = {}
    for letter in string.ascii_lowercase:
        s_ = s[:] # copies to avoid mutating
        s_ = s.replace(letter, '').replace(letter.upper(), '')
        s_ = reduce(destroy, s_)
        lengths[len(s_)] = letter
    num = min(lengths.keys())
    return str('Removing the letter ' + str(lengths[num]) + ' yields a string of length ' + str(num))
    

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))
