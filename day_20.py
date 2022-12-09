#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from enum import Enum
from collections import deque

if len(sys.argv) == 1:
    sys.argv += ["input_20"]

class Direction(Enum):
    NORTH = 'N'
    WEST = 'W'
    EAST = 'E'
    SOUTH = 'S'
    
    def next(self, p):
        if self == Direction.NORTH:
            return (p[0], p[1] + 1)
        if self == Direction.EAST:
            return (p[0] + 1, p[1])
        if self == Direction.SOUTH:
            return (p[0], p[1] - 1)
        if self == Direction.WEST:
            return (p[0] - 1, p[1])

def work_p1_p2(line):
    line = line.strip()[1:-1]
    
    stack = deque()
    p = (0, 0)
    distances = {p: 0}
    p_prev = p
    for c in line:
        if c == '(':
            stack.append((p, p_prev))
            p_prev = p
        elif c == ')':
            p, p_prev = stack.pop()
        elif c == '|':
            p, p_prev = stack[-1]
        else: #c in ['N', 'E', 'W', 'S']:
            p = Direction(c).next(p)
            if distances.get(p, 0) != 0:
                distances[p] = min(distances[p], distances[p_prev] + 1)
            else:
                distances[p] = distances.get(p_prev, 0) + 1
            p_prev = p
    
    return (max(distances.values()), sum(1 for d in distances.values() if d >= 1000))
    

sample_1="^WNE$"
sample_2="^ENWWW(NEEE|SSE(EE|N))$"
sample_3="^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"

def test_p1():
    assert work_p1_p2(sample_1)[0] == 3
    assert work_p1_p2(sample_2)[0] == 10
    assert work_p1_p2(sample_3)[0] == 18
test_p1()

def p1():
    with fileinput.input() as inp:
        print(work_p1_p2(inp.readline()))
p1()
