"""
Advent of Code 2020
Day 4: Passport Processing
"""

REQUIRED_FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}


def get_all_passports(puzzle_input):
    all_passports = []
    passport = []
    for line in puzzle_input:
        if line == "":
            # break between passports
            all_passports.append(passport)
            passport = []
        else: 
            # continuation of current passport
            passport.extend(line.split())
    all_passports.append(passport)
    return all_passports


def get_fields(passport):
    fields = {}
    for field in passport:
        field_type, value = field.split(":")
        fields[field_type] = value
    return fields


def contains_all_required_fields(passport):
    fields = get_fields(passport)
    field_types = fields.keys()
    return REQUIRED_FIELDS.issubset(field_types)


def valid_hex(s):
    try:
        _ = int(s, 16)
        return True
    except:
        return False


def valid_values(passport):
    fields = get_fields(passport)

    # birth year
    byr = int(fields['byr'])
    if not (1920 <= byr <= 2002):
        return False

    # issue year
    iyr = int(fields['iyr'])
    if not (2010 <= iyr <= 2020):
        return False

    # expiration year
    eyr = int(fields['eyr'])
    if not (2020 <= eyr <= 2030):
        return False

    # height
    hgt_val, hgt_unit = int(fields['hgt'][:-2]), fields['hgt'][-2:]
    if hgt_unit == "cm":
        if not (150 <= hgt_val <= 193):
            return False
    elif hgt_unit == "in":
        if not (59 <= hgt_val <= 76):
            return False
    else:
        return False
    
    # hair color
    hcl = fields['hcl']
    if hcl[0] != "#":
        return False
    if not valid_hex(hcl[1:]):
        return False

    # eye color
    ecl = fields['ecl']
    if ecl not in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
        return False

    # passport ID
    pid = fields['pid']
    if len(pid) != 9:
        return False

    return True


def count_valid_passports(puzzle_input, constraints):
    valid_passports = 0
    passports = get_all_passports(puzzle_input)
    for passport in passports:
        if contains_all_required_fields(passport):
            if (not constraints) or (constraints and valid_values(passport)):
                valid_passports += 1
    return valid_passports


def solve_part_1(puzzle_input):
    return count_valid_passports(puzzle_input, False)


def solve_part_2(puzzle_input):
    return count_valid_passports(puzzle_input, True)
