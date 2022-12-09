#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

if len(sys.argv) == 1:
    sys.argv += ["input_03"]

def work_p1_p2(lines):
    parse_re = re.compile("#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
    fabric = {}
    overlaps_lists = {}
    
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        match = parse_re.match(line)
        claim_id, start_x, start_y, width, height = map(int, match.groups())
        
        overlaps_lists[claim_id] = set()
        
        for x in range(start_x, start_x + width):
            for y in range(start_y, start_y + height):
                l = fabric.get((x, y), list())
                if len(l) > 0:
                    for claim_number in l:
                        overlaps_lists[claim_number].add(claim_id)
                        overlaps_lists[claim_id].add(claim_number)
                l.append(claim_id)
                fabric[x,y] = l
    
    r1 = sum(1 for x, y in fabric.keys() if len(fabric[x,y]) >= 2)
    r2 = next(claim_id for claim_id in overlaps_lists if len(overlaps_lists[claim_id]) == 0)
    return (r1, r2)

def p1_p2():
    print(work_p1_p2(fileinput.input()))
p1_p2()
