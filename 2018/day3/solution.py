import re

claims = open('2018/day3/day3.txt').read()
pattern = r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)'
claims = [[int(y) for y in x] for x in re.findall(pattern,claims)]
           
def generate_fabric():
    areas = dict.fromkeys(range(1000)) # keys are columns (left and right)
    for key in areas.keys():
        areas[key] = dict.fromkeys(range(1000)) # values are dicts that map row (up and down) to value
    return areas
    

def part_1():
    areas = generate_fabric()
    s = 0
    for c in claims:
        for h in range(c[1],c[1]+c[3]):
            for v in range(c[2],c[2]+c[4]):
                if areas[h][v] == None:
                    areas[h][v] = False # one claim covers
                elif areas[h][v] == False:
                    areas[h][v] = True # at least one overlap
                    s += 1
    return s
    

def part_2():
    areas = generate_fabric()
    for c in claims:
        claim_id = c[0]
        for h in range(c[1],c[1]+c[3]):
            for v in range(c[2],c[2]+c[4]):
                if areas[h][v] == None:
                    areas[h][v] = [claim_id] # one claim covers
                else:
                    areas[h][v].append(claim_id) # at least one overlap
                    
    vals = []
    for i in range(1000):
        [vals.append(val) for val in areas[i].values() if val]
                
    claimed = dict.fromkeys(range(1, len(claims)+1), False)
    for i, val in enumerate(vals):
        if len(val) > 1:
            for v in val:
                claimed[v] = True
    return list(claimed.keys())[list(claimed.values()).index(False)]
    

print("Part 1: {}".format(part_1()))
print("Part 2: {}".format(part_2()))
