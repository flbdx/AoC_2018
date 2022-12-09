#!/usr/bin/python3
#encoding: UTF-8

# this one does the job, but it's not satisfying as it's a randomized search

import fileinput
import sys
import re
import copy

if len(sys.argv) == 1:
    sys.argv += ["input_24"]

sample_input ="""Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4""".splitlines()

class Group:
    def __init__(self, line, side, id_, boost=0):
        global_rxp = re.compile("([0-9]+) units each with ([0-9]+) hit points (\([^)]+\) )?with an attack that does ([0-9]+) ([a-z]+) damage at initiative ([0-9]+)")
        weak_rxp = re.compile("weak to ([a-z, ]+)")
        immune_rxp = re.compile("immune to ([a-z, ]+)")
        global_match = global_rxp.match(line)
        group_weak_immune = global_match.group(3)
        if group_weak_immune != None:
            weak_match = weak_rxp.search(group_weak_immune)
            immune_match = immune_rxp.search(group_weak_immune)
        
        self.side = side
        self.N = int(global_match.group(1))
        self.HP = int(global_match.group(2))
        self.D = int(global_match.group(4)) + boost
        self.DTYPE = global_match.group(5)
        self.INI = int(global_match.group(6))
        self.WEAK = [] if group_weak_immune == None or weak_match == None else weak_match.group(1).split(", ")
        self.STR = [] if group_weak_immune == None or immune_match == None else immune_match.group(1).split(", ")
        
        self.id = id_
    
    #def __repr__(self):
        #return "{ " + self.side + ":" + repr(self.id) + " N:" + repr(self.N) + " HP:" + repr(self.HP) + " D:" + repr(self.D) + " EP:" + repr(self.effective_power()) + " DTYPE:" + self.DTYPE + " INI:" + repr(self.INI) + " WEAK:" + repr(self.WEAK) + " STR:" + repr(self.STR) + " }"
        ##return "{ " + self.side + ":" + repr(self.id) + " N:" + repr(self.N) + " HP:" + repr(self.HP) + " D:" + repr(self.D) + " EP:" + repr(self.effective_power()) + " }"
    
    def effective_power(self):
        return self.N * self.D
    
    def predict_damage(self, attacker):
        damage = attacker.effective_power()
        if attacker.DTYPE in self.WEAK:
            damage *= 2
        elif attacker.DTYPE in self.STR:
            damage = 0
        return damage
    
    def receive_damage(self, attacker):
        damage = self.predict_damage(attacker)
        deads = damage // self.HP
        deads = self.N if deads > self.N else deads
        self.N -= deads
        return deads
    
    def is_weak_against(self, damage_type):
        return damage_type in self.WEAK
    
    def is_immune_to(self, damage_type):
        return damage_type in self.STR

def lets_fight(immune_groups, infection_groups):
    def sort_key_ep_ini(group):
        return (-group.effective_power(), -group.INI)
    def sort_key_ini(group):
        return -group.INI
    def sort_key_damage(attacker, group):
        predicted_damage = attacker.effective_power()
        if group.is_weak_against(attacker.DTYPE):
            predicted_damage *= 2
        elif group.is_immune_to(attacker.DTYPE):
            predicted_damage = 0
        return (-predicted_damage, -group.effective_power(), -group.INI)
    
    while True:
        targets = {g:None for g in immune_groups + infection_groups}
        attacked_by = {g:None for g in immune_groups + infection_groups}
        
        # TARGET SELECTION PHASE
        for sides in ((immune_groups, infection_groups), (infection_groups, immune_groups)):
            groups_by_ep_ini = sorted(sides[0], key=sort_key_ep_ini)
            for attacker in groups_by_ep_ini:
                groups_by_damage = sorted(sides[1], key=lambda g : sort_key_damage(attacker, g))
                for target in groups_by_damage:
                    if attacked_by[target] == None and target.predict_damage(attacker) > 0:
                        targets[attacker] = target
                        attacked_by[target] = attacker
                        break
        
        # ATTACKING PHASE
        total_deads = 0
        sorted_groups = sorted(immune_groups + infection_groups, key=sort_key_ini)
        for attacker in sorted_groups:
            if attacker.N == 0 or targets[attacker] == None: #is_ded or no homie to play with
                continue
            total_deads += targets[attacker].receive_damage(attacker)
        
        # BURRY THE DEADS
        immune_groups = [g for g in immune_groups if g.N > 0]
        infection_groups = [g for g in infection_groups if g.N > 0]
        
        if total_deads == 0:
            # it does append once with my input
            # for ex not enough damage to kill at least one unit
            #print("TIE")
            return False
        
        #print("--------------------------------------")
        if len(immune_groups) == 0 or len(infection_groups) == 0:
            break
    return True

def read_inputs(inputs, boost=0):
    immune_groups = []
    infection_groups = []
    
    it = iter(inputs)
    next(it)
    id_ = 0
    while (True):
        line = next(it).strip()
        if len(line) == 0:
            break
        id_ += 1
        immune_groups.append(Group(line, "Immune", id_, boost))
    
    next(it)
    id_ = 0
    while (True):
        line = next(it, None)
        if line == None:
            break
        line = line.strip()
        if len(line) == 0:
            break
        id_ += 1
        infection_groups.append(Group(line, "Infection", id_))
    
    return (immune_groups, infection_groups)

def work_p1(inputs):
    immune_groups, infection_groups = read_inputs(inputs)
    lets_fight(immune_groups, infection_groups)
    
    return sum(g.N for g in immune_groups + infection_groups)

def work_p2(inputs, starting_boost=1):
    inputs = list(inputs)
    boost = starting_boost
    while True:
        immune_groups, infection_groups = read_inputs(inputs, boost)
        
        if lets_fight(immune_groups, infection_groups):
            #print(boost, immune_groups, infection_groups)
            rem = sum(g.N for g in immune_groups)
            if rem > 0:
                return rem
        boost += 1

def test_p1():
    assert(work_p1(sample_input) == 5216)
test_p1()

def p1():
    print(work_p1(fileinput.input()))
p1()

def test_p2():
    assert(work_p2(sample_input, 1570) == 51)
test_p2()

def p2():
    print(work_p2(fileinput.input()))
p2()
