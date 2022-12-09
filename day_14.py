#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_14"]


def work_p1(n_recipes):
    recipes = [3, 7]
    elf_0 = 0
    elf_1 = 1
    
    while len(recipes) < n_recipes + 10:
        new_recipes = recipes[elf_0] + recipes[elf_1]
        recipes += list(map(int, str(new_recipes)))
        elf_0 = (elf_0 + 1 + recipes[elf_0]) % len(recipes)
        elf_1 = (elf_1 + 1 + recipes[elf_1]) % len(recipes)
    
    return "".join(repr(i) for i in recipes[n_recipes:n_recipes + 10])

def work_p2(target):
    recipes = "37"
    elf_0 = 0
    elf_1 = 1
    target_len = len(target)
    map_int = {"0":0, "1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9}
    
    while True:
        new_recipes = map_int[recipes[elf_0]] + map_int[recipes[elf_1]]
        recipes += str(new_recipes)
        idx = recipes.rfind(target, len(recipes) - target_len - 2)
        if idx != -1:
            return idx
        elf_0 = (elf_0 + 1 + map_int[recipes[elf_0]]) % len(recipes)
        elf_1 = (elf_1 + 1 + map_int[recipes[elf_1]]) % len(recipes)

def test_p1():
    assert work_p1(9) == "5158916779"
    assert work_p1(2018) == "5941429882"
test_p1()

def test_p2():
    assert work_p2("59414") == 2018
test_p2()

def p1():
    with fileinput.input() as inp:
        print(work_p1(int(inp.readline().strip())))
p1()

def p2():
    with fileinput.input() as inp:
        print(work_p2(inp.readline().strip()))
p2()
