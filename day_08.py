#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from types import SimpleNamespace
from collections import deque

if len(sys.argv) == 1:
    sys.argv += ["input_08"]

class Node(SimpleNamespace): pass

def parse_node(numbers):
    n_children = numbers.popleft()
    n_meta = numbers.popleft()
    children = [parse_node(numbers) for n in range(n_children)]
    meta = [numbers.popleft() for n in range(n_meta)]
    return SimpleNamespace(children=children, meta=meta)

def parse_tree(line):
    numbers = deque(map(int, line.strip().split(" ")))
    return parse_node(numbers)

def p1():
    with fileinput.input() as inp:
        tree = parse_tree(inp.readline())
        
        queue = [tree]
        total = 0
        while len(queue) != 0:
            e = queue.pop(0)
            total += sum(e.meta)
            queue += e.children
        print(total)
p1()

def value(node):
    if len(node.children) > 0:
        return sum(value(node.children[m-1]) for m in node.meta if m <= len(node.children))
    else:
        return sum(node.meta)

def p2():
    with fileinput.input() as inp:
        tree = parse_tree(inp.readline())
        print(value(tree))
p2()
