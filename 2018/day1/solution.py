frequencies = open('2018/day1/day1.txt').readlines()

def part_1():
    return sum([int(x) for x in frequencies])


def part_2():
    nums = [int(x) for x in frequencies]
    sums = set()
    s = 0 # current running sum
    i = 0 # current index
    while True:
        s += nums[i%len(nums)]
        if s not in sums:
            sums.add(s)
            i += 1
        else:
            return s


print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))
