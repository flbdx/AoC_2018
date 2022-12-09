#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_11"]

def power_level(x, y, serial):
    rack_id = x + 10
    p = (y * rack_id + serial) * rack_id
    p = (p // 100) % 10
    p -= 5
    return p

def setup_grid(serial):
    grid = {}
    for y in range(1, 301):
        for x in range(1, 301):
            grid[x,y] = power_level(x, y, serial)
    return grid

def work_p1(line):
    serial = int(line.strip())
    grid = setup_grid(serial)
    
    def cell_level(x, y):
        return sum(sum(grid[x_,y_] for x_ in range(x, x+3)) for y_ in range(y, y+3))
    
    max_power_level = None
    max_power_level_cell = None
    for y in range(1, 301 - 2):
        for x in range(1, 301 - 2):
            p = cell_level(x, y)
            if max_power_level == None or p > max_power_level:
                max_power_level = p
                max_power_level_cell = (x,y)
    return (max_power_level, max_power_level_cell)

def work_p2(line):
    serial = int(line.strip())
    grid = setup_grid(serial)
    
    # https://en.wikipedia.org/wiki/Summed-area_table
    partial_sums = {}
    for y in range(1, 301):
        for x in range(1, 301):
            partial_sums[x,y] = grid[x,y] + partial_sums.get((x-1, y), 0) + partial_sums.get((x, y-1), 0) - partial_sums.get((x-1, y-1), 0)
    
    def cell_level(x, y, c_len):
        return partial_sums[x + c_len - 1, y + c_len - 1] + partial_sums.get((x - 1, y - 1), 0) - partial_sums.get((x - 1, y + c_len - 1), 0) - partial_sums.get((x + c_len - 1, y - 1), 0)
    
    max_power_level = None
    max_power_level_cell = None
    for c_len in range(1, 301):
        for y in range(1, 301 - c_len + 1):
            for x in range(1, 301 - c_len + 1):
                p = cell_level(x, y, c_len)
                if max_power_level == None or p > max_power_level:
                    max_power_level = p
                    max_power_level_cell = (x, y, c_len)
    return (max_power_level, max_power_level_cell)

def p1():
    with fileinput.input() as inp:
        print(work_p1(inp.readline()))
p1()

def p2():
    with fileinput.input() as inp:
        print(work_p2(inp.readline()))
p2()
