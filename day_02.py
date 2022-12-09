#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import Counter
from itertools import combinations

if len(sys.argv) == 1:
    sys.argv += ["input_02"]

def work_p1(lines):
    n_doubles = 0
    n_triples = 0
    for line in lines:
        counter = Counter(line.strip())
        double, triple = False, False
        for c, n in counter.items():
            if n == 2:
                double = True
            elif n == 3:
                triple = True
        n_doubles += double
        n_triples += triple
    
    return n_doubles * n_triples

def p1():
    print(work_p1(fileinput.input()))
p1()
                
def work_p2(lines):
    lines = [l.strip() for l in lines]
    
    for s1, s2 in combinations(lines, 2):
        n_diffs = 0
        for i in range(min(len(s1), len(s2))):
            if s1[i] != s2[i]:
                n_diffs += 1
        if n_diffs == 1:
            s = ""
            for i in range(min(len(s1), len(s2))):
                if s1[i] == s2[i]:
                    s += s1[i]
            return s
            

def p2():
    print(work_p2(fileinput.input()))
p2()
