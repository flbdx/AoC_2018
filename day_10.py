#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re
from types import SimpleNamespace

sample="""position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_10"]

class Particle(SimpleNamespace):
    def step(self):
        self.x += self.vx
        self.y += self.vy

def read_input(lines):
    re_int = re.compile("[-]?[0-9]+")
    particles = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        ints = list(map(int, re_int.findall(line)))
        particles.append(Particle(x=ints[0],y=ints[1],vx=ints[2], vy=ints[3]))
    return particles

def test(particles):
    l = len({p.y for p in particles})
    if l >=8 and l <= 10: # test hauteur d'1 ligne de texte
        # vérifier un peu plus le 1er caractère
        min_x = min(p.x for p in particles)
        set_y = set()
        for x in range(6): # largeur d'un char
            set_y.update({p.y for p in particles if p.x == min_x + x})
        return len(set_y) == l
    return False

def print_particles(particles):
    points = {(p.x,p.y) for p in particles}
    min_x = min(p.x for p in particles)
    max_x = max(p.x for p in particles)
    min_y = min(p.y for p in particles)
    max_y = max(p.y for p in particles)
    s = ""
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            s += '*' if (x,y) in points else ' '
        s += "\n"
    print(s)

def work_p1(lines, max_t = 20):
    particles = read_input(lines)
    for t in range(max_t):
        if test(particles):
            print_particles(particles)
            print(t)
            break
        for p in particles:
            p.step()

def test_p1():
    work_p1(sample, 5)
test_p1()

def p1():
    work_p1(fileinput.input(), 20000)
p1()
