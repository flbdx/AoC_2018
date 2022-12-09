#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from enum import Enum
from types import SimpleNamespace

if len(sys.argv) == 1:
    sys.argv += ["input_13"]

sample_13 = """/->-\\        
|   |  /----\\
| /-+--+-\  |
| | |  | v  |
\\-+-/  \\-+--/
  \\------/   """.splitlines()

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    
    def turn_left(self):
        return Direction((self.value - 1) % 4)
    def turn_right(self):
        return Direction((self.value + 1) % 4)
    
    def next(self, p):
        if self == Direction.UP:
            return (p[0], p[1] - 1)
        if self == Direction.RIGHT:
            return (p[0] + 1, p[1])
        if self == Direction.DOWN:
            return (p[0], p[1] + 1)
        if self == Direction.LEFT:
            return (p[0] - 1, p[1])

class Cart(SimpleNamespace): pass

class World(object):
    def __init__(self, lines):
        self.world = {}
        self.carts = []
        for y, line in enumerate(lines):
            line = line.rstrip()
            if len(line) == 0:
                continue
            for x, c in enumerate(line):
                if c in "/\\|-+":
                    self.world[x,y] = c
                elif c in "<>":
                    self.world[x,y] = "-"
                    cart = Cart(p=(x,y), d=(Direction.LEFT if c == "<" else Direction.RIGHT), state=0)
                    self.carts.append(cart)
                elif c in "v^":
                    self.world[x,y] = "|"
                    cart = Cart(p=(x,y), d=(Direction.DOWN if c == "v" else Direction.UP), state=0)
                    self.carts.append(cart)
    
    def run_p1(self):
        while True:
            sorted_carts = sorted(self.carts, key=lambda c: (c.p[1], c.p[0]))
            for c in sorted_carts:
                c.p = c.d.next(c.p)
                
                if c.p in set(c_.p for c_ in self.carts if c_ != c):
                    return c.p
                
                w = self.world[c.p]
                if w == "/" and c.d in [Direction.UP,  Direction.DOWN] or w == "\\" and c.d in [Direction.RIGHT,  Direction.LEFT]:
                    c.d = c.d.turn_right()
                elif w == "/" and c.d in [Direction.RIGHT,  Direction.LEFT] or w == "\\" and c.d in [Direction.UP,  Direction.DOWN]:
                    c.d = c.d.turn_left()
                elif w == "+":
                    if c.state == 0:
                        c.d = c.d.turn_left()
                        c.state += 1
                    elif c.state == 1:
                        c.state += 1
                    elif c.state == 2:
                        c.d = c.d.turn_right()
                        c.state = 0
    
    def run_p2(self):
        while len(self.carts) > 1:
            sorted_carts = sorted(self.carts, key=lambda c: (c.p[1], c.p[0]))
            destroyed = []
            for c in sorted_carts:
                if c in destroyed:
                    continue
                c.p = c.d.next(c.p)
            
                crash = False
                for c2 in sorted_carts:
                    if c == c2:
                        continue
                    if c.p == c2.p:
                        destroyed += [c, c2]
                        crash = True
                        break
                
                if crash:
                    continue
                
                w = self.world[c.p]
                if w == "/" and c.d in [Direction.UP,  Direction.DOWN] or w == "\\" and c.d in [Direction.RIGHT,  Direction.LEFT]:
                    c.d = c.d.turn_right()
                elif w == "/" and c.d in [Direction.RIGHT,  Direction.LEFT] or w == "\\" and c.d in [Direction.UP,  Direction.DOWN]:
                    c.d = c.d.turn_left()
                elif w == "+":
                    if c.state == 0:
                        c.d = c.d.turn_left()
                        c.state += 1
                    elif c.state == 1:
                        c.state += 1
                    elif c.state == 2:
                        c.d = c.d.turn_right()
                        c.state = 0
            self.carts = [c for c in self.carts if not c in destroyed]
        
        return self.carts[0].p

def test_p1():
    w = World(sample_13)
    assert w.run_p1() == (7,3)
test_p1()

def p1():
    w = World(fileinput.input())
    print(w.run_p1())
p1()

def p2():
    w = World(fileinput.input())
    print(w.run_p2())
p2()
