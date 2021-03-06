filename = '2020/day4/day4.txt'
puzzle_input = open(filename).readlines()

REQUIRED_FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

def get_passports():
    passports = []
    passport = ''
    for line in puzzle_input:
        if line == '\n': # break between passports
            passport = passport.replace('\n', ' ').split()
            passports.append(passport)
            passport = ''
        else: # continuation of current passport
            passport += line
    passport = passport.replace('\n', ' ').split()
    passports.append(passport)
    return passports

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
    valid_byr = 1920 <= int(fields['byr']) <= 2002
    valid_iyr = 2010 <= int(fields['iyr']) <= 2020
    valid_eyr = 2020 <= int(fields['eyr']) <= 2030
    valid_hgt = (fields['hgt'][-2:] == "cm" and 150 <= int(fields['hgt'][:-2]) <= 193) \
        or (fields['hgt'][-2:] == "in" and 59 <= int(fields['hgt'][:-2]) <= 76)
    valid_hcl = len(fields['hcl']) == 7 and fields['hcl'][0] == '#' and valid_hex(fields['hcl'][1:])
    valid_ecl = fields['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
    valid_pid = len(fields['pid']) == 9
    all_valid = valid_byr and valid_iyr and valid_eyr and valid_hgt and valid_hcl and valid_ecl and valid_pid
    return all_valid

def count_valid_passports(constraints):
    valid_passports = 0
    passports = get_passports()
    for passport in passports:
        if contains_all_required_fields(passport):
            if (not constraints) or (constraints and valid_values(passport)):
                valid_passports += 1
    return valid_passports

def part_1():
    return count_valid_passports(False)

def part_2():
    return count_valid_passports(True)

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))
