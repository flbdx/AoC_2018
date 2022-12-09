#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_06"]

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def work_p1(lines):
    coordinates = {}
    all_labels = set()
    n = 0
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        x, y = map(int, line.split(", "))
        coordinates[n] = (x, y)
        all_labels.add(n)
        n += 1

    min_x = min(x for x, y in coordinates.values())
    max_x = max(x for x, y in coordinates.values())
    min_y = min(y for x, y in coordinates.values())
    max_y = max(y for x, y in coordinates.values())
    
    distances = {}
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            p = (x, y)
            distances[p] = {n:manhattan(p, c) for n, c in coordinates.items()}
            m = min(distances[p].values())
            distances[p] = {n for n, d in distances[p].items() if d == m}
            if len(distances[p]) > 1:
                distances[p] = None
            else:
                distances[p] = distances[p].pop()
    
    all_labels.difference_update(*((distances[x, min_y], distances[x, max_y]) for x in range(min_x, max_x + 1)))
    all_labels.difference_update(*((distances[min_x, y], distances[max_x, y]) for y in range(min_y, max_y + 1)))
    
    areas = {label: sum(1 for x, y in distances if distances[x, y] == label) for label in all_labels}
    return max(areas.values())

def work_p2(lines, limit=10000):
    coordinates = {}
    all_labels = set()
    n = 0
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        x, y = map(int, line.split(", "))
        coordinates[n] = (x, y)
        all_labels.add(n)
        n += 1

    min_x = min(x for x, y in coordinates.values())
    max_x = max(x for x, y in coordinates.values())
    min_y = min(y for x, y in coordinates.values())
    max_y = max(y for x, y in coordinates.values())
    
    distances = {}
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            p = (x, y)
            distances[p] = sum(manhattan(p, c) for n, c in coordinates.items())
    return sum(1 for v in distances.values() if v < limit)


def p1():
    print(work_p1(fileinput.input()))
p1()
def p2():
    print(work_p2(fileinput.input()))
p2()
                
      
