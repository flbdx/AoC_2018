#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque, OrderedDict

if len(sys.argv) == 1:
    sys.argv += ["input_18"]

def parse_input(lines):
    world = OrderedDict()
    for y, line in enumerate(lines):
        line = line.strip()
        if len(line) == 0:
            continue
        for x, c in enumerate(line):
            world[x,y] = c
    return world

class W(object):
    def adjacents(p):
        return [(p[0], p[1] + 1), (p[0], p[1] - 1), (p[0] - 1, p[1]), (p[0] + 1, p[1]),
                (p[0] + 1, p[1] + 1), (p[0] + 1, p[1] - 1), (p[0] - 1, p[1] + 1), (p[0] - 1 , p[1] - 1)]

def step(world):
    n_world = OrderedDict()
    total_trees = 0
    total_yards = 0
    for p, v in world.items():
        n_yards = 0
        n_trees = 0
        for pa in W.adjacents(p):
            if world.get(pa, None) == '#':
                n_yards += 1
            elif world.get(pa, None) == '|':
                n_trees += 1
        if v == '.':
            n_world[p] = '|' if n_trees >= 3 else v
        elif v == '|':
            n_world[p] = '#' if n_yards >= 3 else v
        else:
            n_world[p] = v if (n_yards >= 1 and n_trees >= 1) else '.'
    return n_world

def work_p1(world, n_minutes=10):
    for minute in range(n_minutes):
        world = step(world)
    
    n_yards = 0
    n_trees = 0
    for p, v in world.items():
        if v == '|':
            n_trees += 1
        elif v == '#':
            n_yards += 1
    return n_trees * n_yards

# assume world is an OrderedDict and that ordered is preserved by step
def world_to_string(world):
    return "".join(world.values())

def work_p2(world, n_minutes=1000000000):
    search_depth = 100
    backlog = deque()
    minute = 0
    cycle_len = -1
    while True:
        world = step(world)
        minute += 1
        s = world_to_string(world)
        try:
            found_idx = backlog.index(s)
            cycle_len = len(backlog) - found_idx
            break
        except:
            pass
        if len(backlog) == search_depth:
            backlog.popleft()
        backlog.append(s)
    
    rem = n_minutes - minute
    rem = rem % cycle_len
    
    for m in range(rem):
        world = step(world)
    
    n_yards = 0
    n_trees = 0
    for p, v in world.items():
        if v == '|':
            n_trees += 1
        elif v == '#':
            n_yards += 1
    return n_trees * n_yards

test_lines=""".#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.""".splitlines()

def test_p1():
    w = parse_input(test_lines)
    assert work_p1(w, 10) == 1147
test_p1()

def p1():
    w = parse_input(fileinput.input())
    print(work_p1(w, 10))
p1()

def p2():
    w = parse_input(fileinput.input())
    print(work_p2(w))
p2()
