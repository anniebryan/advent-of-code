modules = open('2019/day1/day1.txt').readlines()
masses = [int(m) for m in modules]


def get_fuel(mass: int) -> int:
    """
    :return:
    >>> get_fuel(1969)
    654
    >>> get_fuel(100756)
    33583
    """
    return int(mass/3) - 2


def get_total_fuel(mass: int) -> int:
    """
    :return:
    >>> get_total_fuel(1969)
    966
    >>> get_total_fuel(100756)
    50346
    """
    initial_fuel = int(mass/3) - 2
    if initial_fuel <= 0:
        return 0
    return initial_fuel + get_total_fuel(initial_fuel)


def part_1():
    return sum([get_fuel(m) for m in masses])


def part_2():
    return sum([get_total_fuel(m) for m in masses])


print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))
