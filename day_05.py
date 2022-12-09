#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_05"]

def react(line):
    line = line.strip()
    i = 0
    while True:
        if i >= len(line) - 1:
            break
        p1 = line[i]
        p2 = line[i+1]
        if (p1.islower() and p2.isupper() and p1.upper() == p2) or (p1.isupper() and p2.islower() and p1.lower() == p2):
            line = line[:i] + line[i+2:]
            i = max(0, i-1)
        else:
            i += 1
    
    return len(line)

def work_p1(line):
    return react(line)

def work_p2(line):
    best = None
    for c in range(26):
        cl = chr(ord('a') + c)
        cu = chr(ord('A') + c)
        r = react(line.replace(cl, "").replace(cu, ""))
        if best == None or r < best:
            best = r
    return best

def p1():
    with fileinput.input() as inp:
        print(work_p1(inp.readline().strip()))
p1()

def p2():
    with fileinput.input() as inp:
        print(work_p2(inp.readline().strip()))
p2()
