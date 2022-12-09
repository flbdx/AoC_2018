#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque

if len(sys.argv) == 1:
    sys.argv += ["input_09"]

def play(n_players, last_marble):
    circle = deque([0])
    scores = {}
    
    for marble in range(1, last_marble + 1):
        if (marble % 23 == 0):
            circle.rotate(6)
            player = marble % n_players
            scores[player] = scores.get(player, 0) + marble + circle.pop()
        else:
            circle.rotate(-2)
            circle.appendleft(marble)

    return max(scores.values())

def test_p1():
    assert play(25, 25) == 32
test_p1()

def p1():
    with fileinput.input() as inp:
        words = inp.readline().strip().split(" ")
        n_players = int(words[0])
        last_marble = int(words[6])
        print(play(n_players, last_marble))
p1()

def p2():
    with fileinput.input() as inp:
        words = inp.readline().strip().split(" ")
        n_players = int(words[0])
        last_marble = int(words[6]) * 100
        print(play(n_players, last_marble))
p2()
    
