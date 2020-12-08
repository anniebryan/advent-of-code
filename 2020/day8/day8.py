filename = '2020/day8/day8.txt'
puzzle_input = open(filename).readlines()

def get_instructions():
    instructions = {}
    for i in range(len(puzzle_input)):
        vals = puzzle_input[i].split()
        instructions[i] = (vals[0], int(vals[1]))
    return instructions

def process_instruction(instructions, i, acc, override = None):
    if override is not None and override[0] == i:
        instruction = (override[1], instructions[i][1])
    else:
        instruction = instructions[i]
    next_i = i + instruction[1] if instruction[0] == 'jmp' else i + 1
    new_acc = acc + instruction[1] if instruction[0] == 'acc' else acc
    return next_i, new_acc

def run_sequence(instructions, override = None):
    seen = {0}
    i, acc = 0, 0
    while True:
        i, acc = process_instruction(instructions, i, acc, override)
        if i in seen: # found cycle
            return (False, acc)
        elif i == len(instructions): # properly terminated
            return (True, acc)
        else:
            seen.add(i)

def try_all_sequences():
    instructions = get_instructions()
    for i in instructions:
        if instructions[i][0] == 'nop': # change to 'jmp'
            override = (i, 'jmp')
            result = run_sequence(instructions, override)
            if result[0]:
                return result[1]
        elif instructions[i][0] == 'jmp': # change to 'nop'
            override = (i, 'nop')
            result = run_sequence(instructions, override)
            if result[0]:
                return result[1]

def part_1():
    instructions = get_instructions()
    return run_sequence(instructions)[1]

def part_2():
    return try_all_sequences()

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))