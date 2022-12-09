#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from types import SimpleNamespace

if len(sys.argv) == 1:
    sys.argv += ["input_15"]

class Unit(SimpleNamespace): pass

class World(object):
    def __init__(self, lines, elf_ap=3):
        self.world = {}
        self.units = {}
        
        for y, line in enumerate(lines):
            line = line.strip()
            if len(line) == 0:
                continue
            for x, c in enumerate(line):
                self.world[x,y] = c
                if c == 'E':
                    self.units[x,y] = SimpleNamespace(p=(x,y), type=c, hp=200, ap=elf_ap)
                elif c == 'G':
                    self.units[x,y] = SimpleNamespace(p=(x,y), type=c, hp=200, ap=3)
        
        #print(self.units)
        
    def sort_key(t):
        return (t.p[1], t.p[0])
    def sort_key_p(p):
        return (p[1], p[0])
    
    def round(self):
        sorted_units = sorted(self.units.keys(), key=World.sort_key_p)
        
        for unit in sorted_units:
            # si l'unité n'a pas été tuée
            if self.world[unit] != '.':
                if not self.play(unit):
                    # fin des combats
                    return False
        return True
    
    def adjacents(p):
        return (p[0]+1, p[1]), (p[0]-1, p[1]), (p[0], p[1]+1), (p[0], p[1]-1)
    
    def unit_in_range_squares(self, unit_p):
        r = []
        for p in World.adjacents(unit_p):
            if self.world[p] == '.':
                r.append(p)
        return r
        
    
    def play(self, unit_p):
        #Each unit begins its turn by identifying all possible targets (enemy units). If no targets remain, combat ends.
        unit = self.units[unit_p]
        other_units_p = sorted([p for p, u in self.units.items() if u.type != unit.type], key=World.sort_key_p)
        if len(other_units_p) == 0:
            return False
        
        #Then, the unit identifies all of the open squares (.) that are in range of each target; these are the squares which are adjacent (immediately up, down, left, or right) to any target and which aren't already occupied by a wall or another unit. Alternatively, the unit might already be in range of a target. If the unit is not already in range of a target, and there are no open squares which are in range of a target, the unit ends its turn.
        squares_in_range = []
        for target_p in other_units_p:
            squares_in_range += self.unit_in_range_squares(target_p)
        
        close_targets = []
        for t_p in other_units_p:
            if t_p in World.adjacents(unit_p):
                close_targets.append(self.units[t_p])
        
        
        #If the unit is already in range of a target, it does not move, but continues its turn with an attack. Otherwise, since it is not in range of a target, it moves.
        if len(close_targets) == 0:
            # move
            # calculer distances entre unit_p et chacun des squares_in_range
            new_p = self.move(unit_p, squares_in_range)
            self.world[unit_p] = '.'
            self.world[new_p] = unit.type
            del self.units[unit_p]
            self.units[new_p] = unit
            unit_p = new_p
            unit.p = new_p
            
            # recalculer les cibles à portée
            close_targets = []
            for t_p in other_units_p:
                if t_p in World.adjacents(unit_p):
                    close_targets.append(self.units[t_p])
        
        if len(close_targets) == 0:
            # aucune cible attaquable
            return True
        
        min_hp = min(t.hp for t in close_targets)
        close_targets = [t for t in close_targets if t.hp == min_hp]
        close_targets = sorted(close_targets, key=World.sort_key)
        target = close_targets[0]
        target.hp -= unit.ap
        if target.hp <= 0:
            self.world[target.p] = '.'
            del self.units[target.p]
        return True
    
    def move(self, unit_p, squares_in_range):
        # trouver les distances
        # flood
        distances = {unit_p: 0}
        queue = [(p, 1) for p in self.unit_in_range_squares(unit_p)]
        while len(queue) > 0:
            p, d = queue.pop(0)
            d_r = distances.get(p, None)
            if d_r != None and d_r <= d:
                continue
            distances[p] = d
            queue += [(p_, d + 1) for p_ in self.unit_in_range_squares(p)]
        
        distances = {p:d for p,d in distances.items() if p in squares_in_range}
        if len(distances) == 0:
            return unit_p
        min_dist = min(distances.values())
        distances = {p:d for p,d in distances.items() if d == min_dist}
        move_target = sorted(distances.keys(), key=World.sort_key_p)[0]
        
        distances = {move_target: 0}
        queue = [(p, 1) for p in self.unit_in_range_squares(move_target)]
        while len(queue) > 0:
            p, d = queue.pop(0)
            d_r = distances.get(p, None)
            if d_r != None and d_r <= d:
                continue
            distances[p] = d
            queue += [(p_, d + 1) for p_ in self.unit_in_range_squares(p)]
        distances = {p:d for p, d in distances.items() if p in self.unit_in_range_squares(unit_p)}
        min_dist = min(distances.values())
        distances = {p:d for p,d in distances.items() if d == min_dist}
        move_step = sorted(distances.keys(), key=World.sort_key_p)[0]
        
        return move_step
    
    def print(self):
        for unit in sorted(self.units.keys(), key=World.sort_key_p):
            print(self.units[unit])
        s=""
        max_x = max(p[0] for p in self.world.keys())
        max_y = max(p[1] for p in self.world.keys())
        for y in range(0, max_y+1):
            for x in range(0, max_x+1):
                s += self.world[x,y]
            s += "\n"
        print(s)

test_1="""#######   
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######""".splitlines()

test_2="""#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########""".splitlines()

def work_p1(lines):
    w = World(lines)
    r = 0
    while True:
        #print(r)
        #w.print()
        if not w.round():
            break
        r += 1
    return r * sum(u.hp for u in w.units.values())

def test_p1():
    assert work_p1(test_1) == 27730
    assert work_p1(test_2) == 18740
test_p1()

def p1():
    with fileinput.input() as inp:
        print(work_p1(inp))
p1()

def work_p2(lines):
    if type(lines) != list:
        lines = list(lines)
    elf_ap = 4
    while True:
        w = World(lines, elf_ap)
        n_elves = len(list(u.p for u in w.units.values() if u.type == 'E'))
        r = 0
        while True:
            #print((r, elf_ap))
            #w.print()
            if not w.round():
                break
            r += 1
        if len(list(u.p for u in w.units.values() if u.type == 'E')) == n_elves:
            return r * sum(u.hp for u in w.units.values())
        elf_ap += 1

def test_p2():
    assert work_p2(test_1) == 4988
    assert work_p2(test_2) == 1140
test_p2()

def p2():
    with fileinput.input() as inp:
        print(work_p2(inp))
p2()
