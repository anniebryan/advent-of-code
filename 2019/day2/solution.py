def get_ints(puzzle_input):
    ints = [int(i) for i in puzzle_input[0].split(",")]
    return ints


def handle_opcode(i: int, ints: list):
    """
    :param i: index of an opcode
    ints[i] is either 1, 2, or 99
    :return: ints = [2,3,0,3,99]
    >>> handle_opcode(0)
    ints becomes [2,3,0,6,99]
    >>> handle_opcode(4)
    'halt'
    """
    new_ints = ints[:]
    opcode = ints[i]
    if opcode == 99:
        return 'halt'
    else:
        if opcode == 1:
            new_ints[ints[i+3]] = ints[ints[i+1]] + ints[ints[i+2]]
        elif opcode == 2:
            new_ints[ints[i+3]] = ints[ints[i+1]] * ints[ints[i+2]]
        else:
            return 'something went wrong'
        return new_ints


def run_until_halt(ints: list):
    i = 0
    prev_ints, new_ints = ints[:], handle_opcode(i, ints)
    while type(new_ints) is not str:
        prev_ints = new_ints
        i += 4
        new_ints = handle_opcode(i, prev_ints)
    if new_ints == 'halt':
        return prev_ints
    else:
        return 'something went wrong'


def part_1(puzzle_input):
    ints = get_ints(puzzle_input)
    ints[1] = 12
    ints[2] = 2
    return run_until_halt(ints)[0]


def part_2(puzzle_input):
    ints = get_ints(puzzle_input)
    desired_output = 19690720
    for noun in range(100):
        for verb in range(100):
            new_ints = ints[:]
            new_ints[1], new_ints[2] = noun, verb
            new_ints = run_until_halt(new_ints)
            if type(new_ints) is not str:
                if new_ints[0] == desired_output:
                    return 100 * noun + verb
