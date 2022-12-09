#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

if len(sys.argv) == 1:
    sys.argv += ["input_16"]

class Machine(object):
#Addition:

    #addr (add register) stores into register C the result of adding register A and register B.
    def test_addr(regs_in, operands):
        v = regs_in.copy()
        v[operands[2]] = v[operands[0]] + v[operands[1]]
        return v
    #addi (add immediate) stores into register C the result of adding register A and value B.
    def test_addi(regs_in, operands):
        v = regs_in.copy()
        v[operands[2]] = v[operands[0]] + operands[1]
        return v

#Multiplication:

    #mulr (multiply register) stores into register C the result of multiplying register A and register B.
    def test_mulr(regs_in, operands):
        v = regs_in.copy()
        v[operands[2]] = v[operands[0]] * v[operands[1]]
        return v
    #muli (multiply immediate) stores into register C the result of multiplying register A and value B.
    def test_muli(regs_in, operands):
        v = regs_in.copy()
        v[operands[2]] = v[operands[0]] * operands[1]
        return v

#Bitwise AND:

    #banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
    def test_bandr(regs_in, operands):
        v = regs_in.copy()
        v[operands[2]] = v[operands[0]] & v[operands[1]]
        return v
    #bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
    def test_bandi(regs_in, operands):
        v = regs_in.copy()
        v[operands[2]] = v[operands[0]] & operands[1]
        return v

#Bitwise OR:

    #borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
    def test_baorr(regs_in, operands):
        v = regs_in.copy()
        v[operands[2]] = v[operands[0]] | v[operands[1]]
        return v
    #bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
    def test_bori(regs_in, operands):
        v = regs_in.copy()
        v[operands[2]] = v[operands[0]] | operands[1]
        return v

#Assignment:

    #setr (set register) copies the contents of register A into register C. (Input B is ignored.)
    def test_setr(regs_in, operands):
        v = regs_in.copy()
        v[operands[2]] = v[operands[0]]
        return v
    #seti (set immediate) stores value A into register C. (Input B is ignored.)
    def test_seti(regs_in, operands):
        v = regs_in.copy()
        v[operands[2]] = operands[0]
        return v

#Greater-than testing:

    #gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
    def test_gtir(regs_in, operands):
        v = regs_in.copy()
        v[operands[2]] = 1 if operands[0] > v[operands[1]] else 0
        return v
    #gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
    def test_gtri(regs_in, operands):
        v = regs_in.copy()
        v[operands[2]] = 1 if v[operands[0]] > operands[1] else 0
        return v
    #gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
    def test_gtrr(regs_in, operands):
        v = regs_in.copy()
        v[operands[2]] = 1 if v[operands[0]] > v[operands[1]] else 0
        return v

#Equality testing:

    #eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
    def test_eqir(regs_in, operands):
        v = regs_in.copy()
        v[operands[2]] = 1 if operands[0] == v[operands[1]] else 0
        return v
    #eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
    def test_eqri(regs_in, operands):
        v = regs_in.copy()
        v[operands[2]] = 1 if v[operands[0]] == operands[1] else 0
        return v
    #eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
    def test_eqrr(regs_in, operands):
        v = regs_in.copy()
        v[operands[2]] = 1 if v[operands[0]] == v[operands[1]] else 0
        return v

def work_p1(lines):
    all_tests = [f for n, f in Machine.__dict__.items() if n.startswith("test_")]
    re_int = re.compile("[-]?[0-9]+")
    
    if type(lines) != list:
        lines = list(lines)
        
    res = 0
    
    while len(lines) != 0:
        line = lines.pop(0)
        line = line.strip()
        if len(line) == 0:
            continue
        
        line_before = None
        line_opcodes = None
        line_after = None
        if line.startswith("Before"):
            line_before = line
            line_opcodes = lines.pop(0).strip()
            line_after = lines.pop(0).strip()
            
            regs_before = list(map(int, re_int.findall(line_before)))
            opcodes = list(map(int, re_int.findall(line_opcodes)))
            regs_after = list(map(int, re_int.findall(line_after)))
            
            n_valids = 0
            for f in all_tests:
                if f(regs_before, opcodes[1:]) == regs_after:
                    n_valids += 1
            if n_valids >= 3:
                res += 1
        else:
            break
    return res

def work_p2(lines):
    all_tests = [f for n, f in Machine.__dict__.items() if n.startswith("test_")]
    re_int = re.compile("[-]?[0-9]+")
    
    if type(lines) != list:
        lines = list(lines)
        
    challenges = {}
    
    while len(lines) != 0:
        line = lines.pop(0)
        line = line.strip()
        if len(line) == 0:
            continue
        
        line_before = None
        line_opcodes = None
        line_after = None
        if line.startswith("Before"):
            line_before = line
            line_opcodes = lines.pop(0).strip()
            line_after = lines.pop(0).strip()
            
            regs_before = list(map(int, re_int.findall(line_before)))
            opcodes = list(map(int, re_int.findall(line_opcodes)))
            regs_after = list(map(int, re_int.findall(line_after)))
            
            challenges[opcodes[0]] = challenges.get(opcodes[0], []) + [(regs_before, regs_after, opcodes[1:])]
        else:
            break
    
    opcodes_funcs = {i:None for i in range(16)}
    tests_to_resolve = all_tests.copy()
    while len(tests_to_resolve) != 0:
        opcodes_candidates = {i: list() for i in range(16) if opcodes_funcs[i] == None}
        for op in opcodes_candidates.keys():
            for f in tests_to_resolve:
                pass_all = True
                for c in challenges[op]:
                    if f(c[0], c[2]) != c[1]:
                        pass_all = False
                        break
                if pass_all:
                    opcodes_candidates[op].append(f)
        for op in opcodes_candidates.keys():
            if len(opcodes_candidates[op]) == 1:
                opcodes_funcs[op] = opcodes_candidates[op][0]
                tests_to_resolve.remove(opcodes_funcs[op])

    regs = [0, 0, 0, 0]
    while len(lines) != 0:
        line = lines.pop(0)
        line = line.strip()
        if len(line) == 0:
            continue
        opcodes = list(map(int, re_int.findall(line)))
        regs = opcodes_funcs[opcodes[0]](regs, opcodes[1:])
    return regs[0]

def p1():
    with fileinput.input() as inp:
        print(work_p1(inp))
p1()

def p2():
    with fileinput.input() as inp:
        print(work_p2(inp))
p2()
