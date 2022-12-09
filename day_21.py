#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

if len(sys.argv) == 1:
    sys.argv += ["input_21"]

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
    def op_banr(self, operands):
        self.registers[operands[2]] = self.registers[operands[0]] & self.registers[operands[1]]
    #bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
    def op_bani(self, operands):
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

def p1():
    m = Machine()
    m.run(fileinput.input(), debug=False, breaks=[28])
    print(m.registers[2])
p1()


#00	seti	123			.			2	## r2 = 123
#01	bani	2			456			2	## r2 &= 426
#02	eqri	2			72			2	## r2 = (r2 == 72)
#03	addr	2			4			4	## ip += r2
#04	seti	0			.			4	## GOTO 01
										###
#05	seti	0			.			2	## r2 = 0
#06	bori	2			65536		5	## r5 = r2 | 65536
#07	seti	5234604		.			2	## r2 = 5234604
#08	bani	5			255			3	## r3 = r5 & 0xFF
#09	addr	2			3			2	## r2 += r3
#10	bani	2			16777215	2	## r2 &= 0xFFFFFF
#11	muli	2			65899		2	## r2 *= 65899
#12	bani	2			16777215	2	## r2 &= 0xFFFFFF
#13	gtir	256			5			3	## if 256 > r5; then GOTO 16; else GOTO 15
#14	addr	3			4			4	##
#15	addi	4			1			4	## GOTO 17
#16	seti	27			.			4	## GOTO 28
#17	seti	0			.			3	## r3 = 0
#18	addi	3			1			1	## r1 = r3 + 1
#19	muli	1			256			1	## r1 *= 256
#20	gtrr	1			5			1	## if r1 > r5; then GOTO 23; else GOTO 22
#21	addr	1			4			4	## 
#22	addi	4			1			4	## GOTO 24
#23	seti	25			.			4	## GOTO 26
#24	addi	3			1			3	## r3 += 1
#25	seti	17			.			4	## GOTO 18
#26	setr	3			.			5	## r5 = r3
#27	seti	7			.			4	## GOTO 08
#28	eqrr	2			0			3	## if r2 == r0; then CRASH; else GOTO 06
#29	addr	3			4			4	##
#30	seti	5			.			4	## GOTO 06

def implem(r0_init=0):
    r0 = r0_init
    r1 = 0
    r2 = 0
    r3 = 0
    r5 = 0
    
    test_values = set()
    last_test_value = None
    
    while True:
        r5 = r2 | 0x10000 #06
        r2 = 5234604 # 07
        while True:
            r3 = r5 % 256 # 08
            r2 = (r2 + r3) % (1<<24)
            r2 = (r2 * 65899) % (1<<24) #12
            
            if 256 > r5: #13
                # GOTO 16; GOTO 28
                #print(r2)
                if r2 in test_values:
                    return last_test_value
                else:
                    last_test_value = r2
                    test_values.add(r2)
                if r2 == r0:
                    #print((r0, r1, r2, r3, "IP", r5))
                    return
                else:
                    break # GOTO 06
            else:
                # GOTO 15; GOTO 17
                r3 = 0
                while True:
                    r1 = 256 * (r3 + 1) # 18, 19
                    if r1 > r5:
                        # GOTO 23; GOTO 26
                        r5 = r3
                        break # goto 08
                    else:
                        # GOTO 22; GOTO 24
                        r3 += 1
                        # goto 18

#implem()
def p2():
    print(implem())
p2()
