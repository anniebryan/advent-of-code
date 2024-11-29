import string

boxes = open('2018/day2/day2.txt').readlines()

def part_1():
    num_2 = 0
    num_3 = 0
    for box in boxes:
        counts = []
        for letter in string.ascii_lowercase:
            count = box.count(letter)
            counts.append(count)
        if 2 in counts:
            num_2 += 1
        if 3 in counts:
            num_3 += 1
    return num_2*num_3


def part_2():
    for i in range(len(boxes)):
        box1 = boxes[i]
        remaining = boxes[i+1:]
        for j in range(len(remaining)):
            box2 = remaining[j]
            different = 0
            for l in range(len(box1)-1): # all 27 letters
                if box1[l]!=box2[l]:
                    different += 1
                    letter = l
            if different == 1:
                return box1[0:letter]+box1[letter+1:]


print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))
