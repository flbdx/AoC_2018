#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from types import SimpleNamespace

if len(sys.argv) == 1:
    sys.argv += ["input_07"]

class Step(SimpleNamespace): pass

def parse_lines(lines):
    steps = {}
    
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        words = line.split(" ")
        step_name, step_dep_name = words[7], words[1]
        
        step = steps.get(step_name, SimpleNamespace(name=step_name, depends_on=set(), enable=set()))
        step_dep = steps.get(step_dep_name, SimpleNamespace(name=step_dep_name, depends_on=set(), enable=set()))
        step.depends_on.add(step_dep_name)
        step_dep.enable.add(step_name)
        steps[step_name] = step
        steps[step_dep_name] = step_dep
    return steps

def work_p1(lines):
    steps = parse_lines(lines)
    record = ""
    while len(steps) != 0:
        candidates = {name for name, step in steps.items() if len(step.depends_on) == 0}
        candidates = sorted(candidates)
        candidate = candidates.pop(0)
        record += candidate
        step_candidate = steps[candidate]
        for s in step_candidate.enable:
            steps[s].depends_on.remove(candidate)
        del steps[candidate]
    return record

def work_p2(lines, max_workers=5, base_duration=60):
    steps = parse_lines(lines)
    record = ""
    workers = {}
    ts = 0
    while len(steps) != 0:
        working_on = list(workers.keys())
        for step in working_on:
            workers[step] -= 1
            if workers[step] == 0:
                for s in steps[step].enable:
                    steps[s].depends_on.remove(step)
                del steps[step]
                del workers[step]
        
        candidates = {name for name, step in steps.items() if len(step.depends_on) == 0 and name not in workers}
        candidates = sorted(candidates)
        while len(workers) != max_workers and len(candidates) > 0:
            candidate = candidates.pop(0)
            workers[candidate] = base_duration + ord(candidate) - ord('A') + 1
        
        ts += 1
    
    return ts - 1
        

def test_p1():
    lines="""Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".splitlines()
    assert work_p1(lines) == "CABDFE"
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    lines="""Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".splitlines()
    assert work_p2(lines, 2, 0) == 15
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
