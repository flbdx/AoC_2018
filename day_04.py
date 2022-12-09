#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re
import datetime

if len(sys.argv) == 1:
    sys.argv += ["input_04"]

def work_p1_p2(lines):
    lines = sorted(list(lines))
    re_line = re.compile("\[(\d+-\d+-\d+ \d+:\d+)\] (.*)$")
    re_guard = re.compile("Guard #(\d+) begins shift")
    
    records = {}
    current_guard = None
    falls_asleep = None
    
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        match_line = re_line.match(line)
    
        date = datetime.datetime.strptime(match_line.group(1), "%Y-%m-%d %H:%M")
        action = match_line.group(2)
        
        match_guard = re_guard.match(action)
        if match_guard:
            current_guard = int(match_guard.group(1))
            if not current_guard in records:
                records[current_guard] = {}
        elif action == "falls asleep":
            falls_asleep = date
        else:
            for m in range(falls_asleep.minute, date.minute):
                records[current_guard][m] = records[current_guard].get(m, 0) + 1
                
    
    total_sleep_time = {}
    for guard in records:
        total_sleep_time[guard] = sum(records[guard].values())
    guard_p1 = next(g for g in total_sleep_time if total_sleep_time[g] == max(total_sleep_time.values()))
    best_min_p1 = next(m for m in records[guard_p1] if records[guard_p1][m] == max(records[guard_p1].values()))
    score_p1 = guard_p1 * best_min_p1
    
    best_p2 = None
    for guard in records:
        for m in records[guard]:
            if best_p2 == None:
                best_p2 = (guard, m, records[guard][m])
            else:
                if records[guard][m] > best_p2[2]:
                    best_p2 = (guard, m, records[guard][m])
    score_p2 = best_p2[0] * best_p2[1]
    
    return (score_p1, score_p2)

def p1_p2():
    print(work_p1_p2(fileinput.input()))
p1_p2()
