#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_01"]

def p1():
    print(sum(int(line.strip()) for line in fileinput.input()))
p1()

def p2():
    s = set([0])
    r = 0
    done = False
    while not done:
        for line in fileinput.input():
            r += int(line.strip())
            if r in s:
                print(r)
                done = True
                break
            s.add(r)
p2()
