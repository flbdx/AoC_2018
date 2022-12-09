#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from enum import Enum
from networkx import Graph, dijkstra_path_length

if len(sys.argv) == 1:
    sys.argv += ["input_22"]

def read_file(lines):
    if type(lines) != list:
        lines = list(lines)
    depth=int(lines[0].split(" ")[1])
    target_x, target_y=tuple(map(int, lines[1].split(" ")[1].split(",")))
    return (depth, (target_x, target_y))

class Item(Enum):
    ClimbingGear = 0
    Torch = 1
    Neither = 2
    
    # return the valid items for the given region's type
    def valid_items(region):
        if region == 0: # rocky
            return [Item.ClimbingGear, Item.Torch]
        elif region == 1: # wet
            return [Item.ClimbingGear, Item.Neither]
        else: # narrow
            return [Item.Torch, Item.Neither]

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    
    def next(self, p):
        if self == Direction.UP:
            return (p[0], p[1] + 1)
        if self == Direction.RIGHT:
            return (p[0] + 1, p[1])
        if self == Direction.DOWN:
            return (p[0], p[1] - 1)
        if self == Direction.LEFT:
            return (p[0] - 1, p[1])

def erosion_map(depth, target, extra = 0):
    target_x, target_y = target[0], target[1]
    
    erosion = {}
    for y in range(0, target_y+extra+1):
        for x in range(0, target_x+extra+1):
            if x == 0 and y == 0:
                geologic_index = 0
            elif x == target_x and y == target_y:
                geologic_index = 0
            elif y == 0:
                geologic_index = x * 16807
            elif x == 0:
                geologic_index = y * 48271
            else:
                geologic_index = erosion[x-1,y] * erosion[x,y-1]
            erosion[x,y] = (geologic_index + depth) % 20183
    
    return erosion

def region_map(erosion_level):
    return {c:(v%3) for c, v in erosion_level.items()}

def risk_level(regions):
    return sum(v for v in regions.values())

sample_input="""depth: 510
target: 10,10
""".splitlines()

def test_p1():
    depth, target = read_file(sample_input)
    erosion = erosion_map(depth, target)
    regions = region_map(erosion)
    assert risk_level(regions) == 114
test_p1()

def p1():
    depth, target = read_file(fileinput.input())
    erosion = erosion_map(depth, target)
    regions = region_map(erosion)
    print(risk_level(regions))
p1()

def work_p2(target, extra_space, regions):
    graph = Graph()
    # each node is a tuple (x, y, item)
    # starting node is (0,0,Torch), target is (target[0],target[1],Torch)
    
    for y in range(0, target[1] + extra_space + 1):
        for x in range(0, target[0] + extra_space + 1):
            r = regions[x,y]
            
            # we can switch with another item, that's one edge
            valid_items = Item.valid_items(r) # always 2 valid items, ie 1 possible transition
            graph.add_edge((x, y, valid_items[0]), (x, y, valid_items[1]), weight=7)
            
            for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                n_x, n_y = direction.next((x,y))
                if n_x >= 0 and n_x <= (target[0] + extra_space) and n_y >= 0 and n_y <= (target[1] + extra_space):
                    # check if equipment is compatilbe with the next space
                    r = regions[n_x, n_y]
                    for item in Item.valid_items(r):
                        if item in valid_items:
                            graph.add_edge((x, y, item), (n_x, n_y, item), weight=1)
    return dijkstra_path_length(graph, (0, 0, Item.Torch), (target[0], target[1], Item.Torch))

def test_p2():
    extra_space=10
    depth, target = read_file(sample_input)
    erosion = erosion_map(depth, target, extra_space)
    regions = region_map(erosion)
    assert work_p2(target, extra_space, regions) == 45
test_p2()

def p2():
    extra_space=100
    depth, target = read_file(fileinput.input())
    erosion = erosion_map(depth, target, extra_space)
    regions = region_map(erosion)
    print(work_p2(target, extra_space, regions))
p2()
