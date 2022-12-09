#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

if len(sys.argv) == 1:
    sys.argv += ["input_19"]

class Machine(object):
    def Machine(self):
        self.reset()
    def reset(self, part2=False):
        self.registers = [0 for i in range(6)]
        if part2:
            self.registers[0] = 1
        self.ip_reg = -1
        self.ip = 0
    
    def run(self, lines, part2=False, breaks=[], debug=False, n_steps=-1):
        self.reset(part2)
        
        if type(lines) != list:
            lines = list(lines)
        
        instructions = []
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            words = line.split(" ")
            if words[0] == "#ip":
                self.ip_reg = int(words[1])
            else:
                op = Machine.__dict__["op_" + words[0]]
                instructions.append((op, [int(w) for w in words[1:]]))
        
        step=0
        while n_steps == -1 or step < n_steps:
            step += 1
            
            if self.ip < 0 or self.ip >= len(instructions):
                break
            if self.ip in breaks:
                break
            
            instr = instructions[self.ip]
            
            if debug:
                prev_ip = self.ip
                prev_regs = self.registers.copy()
                prev_instr = instr[0].__name__
            
            if self.ip_reg >= 0:
                self.registers[self.ip_reg] = self.ip
            
            instr[0](self, instr[1])
            
            if debug:
                print((prev_ip, prev_regs, prev_instr, instr[1], self.registers))

            if self.ip_reg >= 0:
                self.ip = self.registers[self.ip_reg]
            
            self.ip += 1
    
    def set_ip_reg(self, operands):
        self.ip_reg = operands[0]
    
#Addition:

    #addr (add register) stores into register C the result of adding register A and register B.
    def op_addr(self, operands):
        self.registers[operands[2]] = self.registers[operands[0]] + self.registers[operands[1]]
    #addi (add immediate) stores into register C the result of adding register A and value B.
    def op_addi(self, operands):
        self.registers[operands[2]] = self.registers[operands[0]] + operands[1]

#Multiplication:

    #mulr (multiply register) stores into register C the result of multiplying register A and register B.
    def op_mulr(self, operands):
        self.registers[operands[2]] = self.registers[operands[0]] * self.registers[operands[1]]
    #muli (multiply immediate) stores into register C the result of multiplying register A and value B.
    def op_muli(self, operands):
        self.registers[operands[2]] = self.registers[operands[0]] * operands[1]

#Bitwise AND:

    #banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
    def op_bandr(self, operands):
        self.registers[operands[2]] = self.registers[operands[0]] & self.registers[operands[1]]
    #bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
    def op_bandi(self, operands):
        self.registers[operands[2]] = self.registers[operands[0]] & operands[1]

#Bitwise OR:

    #borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
    def op_baorr(self, operands):
        self.registers[operands[2]] = self.registers[operands[0]] | self.registers[operands[1]]
    #bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
    def op_bori(self, operands):
        self.registers[operands[2]] = self.registers[operands[0]] | operands[1]

#Assignment:

    #setr (set register) copies the contents of register A into register C. (Input B is ignored.)
    def op_setr(self, operands):
        self.registers[operands[2]] = self.registers[operands[0]]
    #seti (set immediate) stores value A into register C. (Input B is ignored.)
    def op_seti(self, operands):
        self.registers[operands[2]] = operands[0]

#Greater-than testing:

    #gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
    def op_gtir(self, operands):
        self.registers[operands[2]] = 1 if operands[0] > self.registers[operands[1]] else 0
    #gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
    def op_gtri(self, operands):
        self.registers[operands[2]] = 1 if self.registers[operands[0]] > operands[1] else 0
    #gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
    def op_gtrr(self, operands):
        self.registers[operands[2]] = 1 if self.registers[operands[0]] > self.registers[operands[1]] else 0

#Equality testing:

    #eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
    def op_eqir(self, operands):
        self.registers[operands[2]] = 1 if operands[0] == self.registers[operands[1]] else 0
    #eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
    def op_eqri(self, operands):
        self.registers[operands[2]] = 1 if self.registers[operands[0]] == operands[1] else 0
    #eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
    def op_eqrr(self, operands):
        self.registers[operands[2]] = 1 if self.registers[operands[0]] == self.registers[operands[1]] else 0

sample_input = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5""".splitlines()

def test_p1():
    m = Machine()
    m.run(sample_input)
    assert m.registers[0] == 6
test_p1()

def p1():
    m = Machine()
    m.run(fileinput.input())
    print(m.registers[0])
#p1()

def debug():
    m = Machine()
    m.run(fileinput.input(), part2=True, debug=True, n_steps=50)
#debug()

def p1_bis():
    m = Machine()
    m.run(fileinput.input(), breaks=[1]) # arrêt sur IP=1
    r1 = m.registers[1]
    ## somme des diviseurs de r1
    r0 = r1
    for r5 in range(1, r1//2+1):
        if (r1%r5) == 0:
            r0 += r5
    print(r0)
p1_bis()

def p2():
    m = Machine()
    m.run(fileinput.input(), part2=True, breaks=[1]) # arrêt sur IP=1
    r1 = m.registers[1]
    ## somme des diviseurs de r1
    r0 = r1
    for r5 in range(1, r1//2+1):
        if (r1%r5) == 0:
            r0 += r5
    print(r0)
p2()


