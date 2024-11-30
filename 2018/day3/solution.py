"""
Advent of Code 2018
Day 3: No Matter How You Slice It
"""

import re

def get_claims(puzzle_input):
    pattern = r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)'
    claims = [[int(y) for y in re.match(pattern, row).groups()] for row in puzzle_input]
    return claims
           
def generate_fabric():
    areas = dict.fromkeys(range(1000)) # keys are columns (left and right)
    for key in areas.keys():
        areas[key] = dict.fromkeys(range(1000)) # values are dicts that map row (up and down) to value
    return areas
    

def part_1(puzzle_input):
    claims = get_claims(puzzle_input)
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
    

def part_2(puzzle_input):
    claims = get_claims(puzzle_input)
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
