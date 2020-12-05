filename = '2020/day2/day2.txt'
puzzle_input = open(filename).readlines()

def get_passwords():
    passwords = []
    for line in puzzle_input:
        info = line.split()
        low, high = info[0].split("-")
        char = info[1][0]
        password = info[2]
        passwords.append((int(low), int(high), char, password))
    return passwords

def get_password_char_count(password, c):
    count = 0
    for char in password:
        if char == c:
            count += 1
    return count

def count_valid_passwords_policy_one():
    """ a password is valid if the number of times the given character appears
    is between low and high inclusive """
    num_valid_passwords = 0
    passwords = get_passwords()
    for password in passwords:
        low, high, c, p = password
        count = get_password_char_count(p, c)
        if count >= low and count <= high:
            num_valid_passwords += 1
    return num_valid_passwords

def get_chars_at(password, i, j):
    return {password[i-1], password[j-1]}

def count_valid_passwords_policy_two():
    """ a password is valid if the given character appears exactly once out of
    the two indices provided (one-indexed) """
    num_valid_passwords = 0
    passwords = get_passwords()
    for password in passwords:
        i, j, c, p = password
        chars = get_chars_at(p, i, j)
        if c in chars and len(chars) == 2:
            num_valid_passwords += 1
    return num_valid_passwords

def part_1():
    num_valid_passwords = count_valid_passwords_policy_one()
    return num_valid_passwords

def part_2():
    num_valid_passwords = count_valid_passwords_policy_two()
    return num_valid_passwords

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))