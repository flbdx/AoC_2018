#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

if len(sys.argv) == 1:
    sys.argv += ["input_17"]

def parse_input(lines):
    world = {}
    re_input = re.compile("([xy])=([0-9]+), [xy]=([0-9]+)..([0-9]+)")
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        re_res = re_input.match(line)
        first_is_x = re_res.group(1) == 'x'
        first_v = int(re_res.group(2))
        second_b = int(re_res.group(3))
        second_e = int(re_res.group(4))
        
        for C in range(second_b, second_e + 1):
            if first_is_x:
                world[first_v, C] = '#'
            else:
                world[C, first_v] = '#'
    
    return world

class W(object):
    def bottom(p):
        return (p[0], p[1] + 1)
    def top(p):
        return (p[0], p[1] - 1)
    def left(p):
        return (p[0] - 1, p[1])
    def right(p):
        return (p[0] + 1, p[1])

def work_p1(world):
    min_x = min(p[0] for p in world.keys())
    max_x = max(p[0] for p in world.keys())
    min_y = min(p[1] for p in world.keys())
    max_y = max(p[1] for p in world.keys())
    
    queue = [(500, 0)]
    world[500, 0] = '|'
    
    def set_zone(p, v):
        nonlocal queue
        nonlocal max_y
        
        if p[1] > max_y:
            return
        
        cv = world.get(p, '.')
        if cv == '#':
            return
        if v == cv:
            return
        world[p] = v
        queue += [W.left(p), W.right(p), W.top(p), W.bottom(p), p]
        
    while len(queue) != 0:
        p_at = queue.pop(0)
        p_at_v = world.get(p_at, '.')
        
        if p_at_v == '.':
            continue
        
        if p_at[1] > max_y:
            continue
        
        if p_at_v == '|':
            if W.bottom(p_at) not in world.keys():
                set_zone(W.bottom(p_at), '|')
        
        if p_at_v == '|':
            # regarder à gauche
            p_check = p_at
            bounded = True
            while True:
                if world.get(p_check, '.') == '#':
                    # mur à gauche
                    break
                if world.get(W.bottom(p_check), '.') not in ['~', '#']:
                    # rien de solide en dessous
                    bounded = False
                    break
                p_check = W.left(p_check)
            p_check = p_at
            while True:
                if world.get(p_check, '.') == '#':
                    # mur à droite
                    break
                if world.get(W.bottom(p_check), '.') not in ['~', '#']:
                    # rien de solide en dessous
                    bounded = False
                    break
                p_check = W.right(p_check)
            if bounded:
                set_zone(p_at, '~')
            
        
        if p_at_v == '|':
            if world.get(W.bottom(p_at), '.') in ['~', '#']:
                set_zone(W.left(p_at), '|')
                set_zone(W.right(p_at), '|')
        
        if p_at_v == '~':
            set_zone(W.left(p_at), '~')
            set_zone(W.right(p_at), '~')

    total_water = 0
    total_stable = 0
    for p, v in world.items():
        if p[1] < min_y or p[1] > max_y:
            continue
        if v in ['~', '|']:
            total_water += 1
        if v == '~':
            total_stable += 1
    
    #for y in range(0, max_y + 1):
        #s = ""
        #for x in range(min_x, max_x + 1):
            #s += world.get((x,y), '.')
        #print(s)
        
    return (total_water, total_stable)

test_lines="""x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504""".splitlines()

def test_p1_p2():
    w = parse_input(test_lines)
    assert work_p1(w) == (57, 29)
test_p1_p2()

def p1_p2():
    w = parse_input(fileinput.input())
    print(work_p1(w))
p1_p2()
        
