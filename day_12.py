#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_12"]

def parse_lines(lines):
    initial_state = None
    rules = {}
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith("initial state: "):
            initial_state = dict(enumerate(line.split(": ")[1]))
        else:
            rule = line.split(" => ")
            c = rule[0][2]
            if not c in rules:
                rules[c] = {}
            rules[c][tuple(rule[0])] = rule[1]
                
    return (initial_state, rules)

def state_to_string(state):
    s = ""
    for i in sorted(state.keys()):
        s += state[i]
    return s

def trim_state(state):
    indexes = range(min(state.keys()), max(state.keys()))
    for i in indexes:
        if state[i] == '.':
            del(state[i])
        else:
            break
    for i in reversed(indexes):
        if state[i] == '.':
            del(state[i])
        else:
            break

def state_to_score(state):
    res = 0
    for idx, v in state.items():
        if v == '#':
            res += idx
    return res

def evolve(state, rules):
    state_ = {}
    indexes = range(min(state.keys()) - 5, max(state.keys()) + 5)
    for i in indexes:
        subseq = tuple(state.get(idx, '.') for idx in range(i-2, i+3))
        state_[i] = '.'
        c = state.get(i, '.')
        for pattern, repl in rules.get(c, {}).items():
            if pattern == subseq:
                state_[i] = repl             
                break
    trim_state(state_)
    return state_

def work_p1(lines):
    state, rules = parse_lines(lines)
    
    for s in range(20):
        state = evolve(state, rules)
    
    return state_to_score(state)

def work_p2(lines):
    state, rules = parse_lines(lines)
    
    trim_state(state)
    
    prev_state_str = state_to_string(state)
    prev_state_score = state_to_score(state)
    s = 0
    while True:
        state = evolve(state, rules)
        state_str = state_to_string(state)
        state_score = state_to_score(state)
        if state_str == prev_state_str:
            break
        prev_state_str = state_str
        s += 1
    state = evolve(state, rules)
    d = state_to_score(state) - state_score
    s += 1
    rem = 50000000000 - s
    return state_score + d * rem


def p1():
    with fileinput.input() as inp:
        print(work_p1(inp))
p1()
 
def p2():
    with fileinput.input() as inp:
        print(work_p2(inp))
p2()
