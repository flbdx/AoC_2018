#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import namedtuple
from itertools import combinations

test_input_0="""0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0""".splitlines()

test_input_1="""-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0""".splitlines()

test_input_2="""1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2""".splitlines()

test_input_3="""1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2""".splitlines()

Point = namedtuple("Point", ["a", "b", "c", "d"])

class Chain:
    def __init__(self, init_set=None):
        self.points = set() if init_set == None else set(init_set)
    def __repr__(self):
        return repr(self.points)
    def add(self, v):
        self.points.add(v)

if len(sys.argv) == 1:
    sys.argv += ["input_25"]

def read_input(inputs):
    r = list()
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            break
        l = [int(v) for v in line.split(",")]
        r.append(Point(*l))
    return r

def manhattan(p1, p2):
    return abs(p1.a - p2.a) + abs(p1.b - p2.b) + abs(p1.c - p2.c) + abs(p1.d - p2.d)

def work_p1(inputs):
    points = read_input(inputs)
    #print(points)
    chains = []
    points_to_chain = {}
    for p in points:
        chain = Chain({p})
        chains.append(chain)
        points_to_chain[p] = chain
    
    for pair in combinations(points, r=2):
        p1, p2 = pair
        d = manhattan(p1, p2)
        #print(repr(p1) + " -- " + repr(p2), d)
        if d <= 3:
            #print(repr(p1) + " -- " + repr(p2), d)
            chain1 = points_to_chain[p1]
            chain2 = points_to_chain[p2]
            if chain1 != chain2:
                for p in chain2.points:
                    chain1.add(p)
                    points_to_chain[p] = chain1
                chains.remove(chain2)
    #print(chains)
    return len(chains)

def test_p1():
    assert(work_p1(test_input_0) == 2)
    assert(work_p1(test_input_1) == 4)
    assert(work_p1(test_input_2) == 3)
    assert(work_p1(test_input_3) == 8)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

