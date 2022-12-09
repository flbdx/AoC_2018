#!/usr/bin/python3
#encoding: UTF-8

# this one does the job, but it's not satisfying as it's a randomized search

import fileinput
import sys
import re
import itertools
import random
random.seed()

if len(sys.argv) == 1:
    sys.argv += ["input_23"]

sample_input_p1 ="""pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1""".splitlines()

sample_input_p2 = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5""".splitlines()

def read_input(lines):
    bots = {}
    re_int = re.compile("[-]?[0-9]+")
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        x,y,z,r = list(map(int, re_int.findall(line)))
        bots[x,y,z] = r
    return bots

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])

def work_p1(bots):
    max_range = max(bots.values())
    best_bot = next(b for b, r in bots.items() if r == max_range)
    in_range = 0
    for b, r in bots.items():
        if manhattan(best_bot, b) <= max_range:
            in_range += 1
    return in_range

def test_p1():
    bots = read_input(sample_input_p1)
    assert work_p1(bots) == 7
test_p1()

def p1():
    bots = read_input(fileinput.input())
    print(work_p1(bots))
p1()


def cube(factor, w=3):
    if w==3:
        return itertools.product((- factor, 0, factor), repeat=3)
    elif (w&1) == 1:
        # we can do a denser grid
        grid = itertools.product(range(-(w//2)*factor, (w//2+1)*factor, factor), repeat=3)
        return [tuple(v//w for v in e) for e in grid]
    else:
        print("w pair")
        sys.exit(25)

def rand_points(factor, w=3, count=27):
    s = set(cube(factor, w))
    for c in range(0, count):
        x = random.randint(-factor, factor)
        y = random.randint(-factor, factor)
        z = random.randint(-factor, factor)
        s.add((x,y,z))
    return s

def work_p2(bots):
    # we will search using a sampling grid, reducing its size after each iteration
    # for each point of the grid, we count how many bots have the point in range
    # we may need multiple runs to find the solution.
    # the "grid" is a set of random points and regular points on a cube
    # I guess it does work because the ranges are huge but I'm not satisfied as
    # it will often not converge towards the best point (although the distance is
    # usually the best)
    
    # let's start by finding the max size
    min_x, max_x = min(x for x,y,z in bots), max(x for x,y,z in bots)
    min_y, max_y = min(y for x,y,z in bots), max(y for x,y,z in bots)
    min_z, max_z = min(z for x,y,z in bots), max(z for x,y,z in bots)

    window_size = max(abs(min_x), abs(max_x), abs(min_y), abs(max_y), abs(min_z), abs(max_z))
    reduce_factor = 0.8
    
    # count the number of nanobots which have p in their range
    def have_in_range(p):
        nonlocal bots
        in_range = 0
        for b,r in bots.items():
            if manhattan(p, b) <= r:
                in_range += 1
        return in_range
    
    grid_size=5
    
    overall_best = None
    
    for iteration in range(5):
        best_in_range = -1      # best number of nanobots in range
        best_distance = None    # best distance from (0,0,0)
        window = window_size
        current_pos = (0,0,0)
        for it in range(3):
            while True:
                for position in rand_points(window, grid_size, grid_size**3):
                    position = tuple(current_pos[i] + position[i] for i in (0,1,2))
                    in_range = have_in_range(position)
                    this_dist = manhattan(position, (0,0,0))
                    if (in_range > best_in_range) or (in_range == best_in_range and this_dist < best_distance):
                        best_in_range = in_range
                        best_distance = this_dist
                        best_position = position
                        #print(window, position, in_range, this_dist)
                current_pos = best_position
                if window == 1:
                    break
                n_window = int(reduce_factor * window)
                if n_window == window:
                    n_window = window - 1
                if n_window == 0:
                    n_window = 1
                window = n_window
        print(current_pos, best_in_range, best_distance)
        overall_best = best_distance if overall_best == None else min(overall_best, best_distance)
    return overall_best

def test_p2():
    bots = read_input(sample_input_p2)
    assert work_p2(bots) == 36
test_p2()

def p2():
    bots = read_input(fileinput.input())
    print(work_p2(bots))
p2()
