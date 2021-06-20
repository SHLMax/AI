# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 20:15:12 2021

@author: Song
"""

import heapq
import copy
    
def heuristic(state):
    count = 0
    state1 = []
    state2 = []
    state3 = []
    for i in range(3):
        for j in range(3):
            state2.append(state[j+3*i])
        state3 = copy.deepcopy(state2)
        state1.append(state3)
        state2.clear()
    for i in range(3):
        for j in range(3):
            if state1[i][j] == 1:
               count = count + abs(i - 0) + abs(j - 0)
            elif state1[i][j] == 2:
               count = count + abs(i - 0) + abs(j - 1)
            elif state1[i][j] == 3:
               count = count + abs(i - 0) + abs(j - 2)
            elif state1[i][j] == 4:
               count = count + abs(i - 1) + abs(j - 0)
            elif state1[i][j] == 5:
               count = count + abs(i - 1) + abs(j - 1)
            elif state1[i][j] == 6:
               count = count + abs(i - 1) + abs(j - 2)
            elif state1[i][j] == 7:
               count = count + abs(i - 2) + abs(j - 0)  
            elif state1[i][j] == 8:
               count = count + abs(i - 2) + abs(j - 1)
    return count   

def print_succ(state):
    state1 = []
    state2 = []
    state3 = []
    state4 = []
    state5 = []
    state6 = []
    state7 = []
    for i in range(3):
        for j in range(3):
            state2.append(state[j+3*i])
        state3 = copy.deepcopy(state2)
        state1.append(state3)
        state2.clear()
    for i in range(3):
        for j in range(3):
            if state1[i][j] == 0:
                if i - 1 >= 0:
                   state4 = copy.deepcopy(state1)
                   state4[i][j] = state4[i-1][j] 
                   state4[i-1][j]  = 0
                   for x in range(3):
                       for y in range(3):
                           state5.append(state4[x][y])
                   state6 = copy.deepcopy(state5)
                   state7.append(state6)
                   state5.clear()
                if i + 1 <= 2:
                   state4 = copy.deepcopy(state1)
                   state4[i][j] = state4[i+1][j] 
                   state4[i+1][j]  = 0
                   for x in range(3):
                       for y in range(3):
                           state5.append(state4[x][y])
                   state6 = copy.deepcopy(state5)
                   state7.append(state6)
                   state5.clear()
                if j + 1 <= 2:
                   state4 = copy.deepcopy(state1)
                   state4[i][j] = state4[i][j+1] 
                   state4[i][j+1]  = 0
                   for x in range(3):
                       for y in range(3):
                           state5.append(state4[x][y])
                   state6 = copy.deepcopy(state5)
                   state7.append(state6)
                   state5.clear()
                if i - 1 >= 0:
                   state4 = copy.deepcopy(state1)
                   state4[i][j] = state4[i][j-1] 
                   state4[i][j-1]  = 0
                   for x in range(3):
                       for y in range(3):
                           state5.append(state4[x][y])
                   state6 = copy.deepcopy(state5)
                   state7.append(state6) 
                   state5.clear()
    state7 = sorted(state7) 
    for row in state7:
        print(row, " h=" + str(heuristic(row)))
    return state7

def get_succ(state):
    state1 = []
    state2 = []
    state3 = []
    state4 = []
    state5 = []
    state6 = []
    state7 = []
    for i in range(3):
        for j in range(3):
            state2.append(state[j+3*i])
        state3 = copy.deepcopy(state2)
        state1.append(state3)
        state2.clear()
    for i in range(3):
        for j in range(3):
            if state1[i][j] == 0:
                if i - 1 >= 0:
                   state4 = copy.deepcopy(state1)
                   state4[i][j] = state4[i-1][j] 
                   state4[i-1][j]  = 0
                   for x in range(3):
                       for y in range(3):
                           state5.append(state4[x][y])
                   state6 = copy.deepcopy(state5)
                   state7.append(state6)
                   state5.clear()
                if i + 1 <= 2:
                   state4 = copy.deepcopy(state1)
                   state4[i][j] = state4[i+1][j] 
                   state4[i+1][j]  = 0
                   for x in range(3):
                       for y in range(3):
                           state5.append(state4[x][y])
                   state6 = copy.deepcopy(state5)
                   state7.append(state6)
                   state5.clear()
                if j + 1 <= 2:
                   state4 = copy.deepcopy(state1)
                   state4[i][j] = state4[i][j+1] 
                   state4[i][j+1]  = 0
                   for x in range(3):
                       for y in range(3):
                           state5.append(state4[x][y])
                   state6 = copy.deepcopy(state5)
                   state7.append(state6)
                   state5.clear()
                if j - 1 >= 0:
                   state4 = copy.deepcopy(state1)
                   state4[i][j] = state4[i][j-1] 
                   state4[i][j-1]  = 0
                   for x in range(3):
                       for y in range(3):
                           state5.append(state4[x][y])
                   state6 = copy.deepcopy(state5)
                   state7.append(state6) 
                   state5.clear()
    state7 = sorted(state7) 
    return state7
        
        
def solve(state):
    opened = []
    closed = {}
    parent = []
    state1 = []
    heapq.heappush(opened,(0+heuristic(state), state, (0, heuristic(state), -1),parent))   
    closed[str(state)] = (0, heuristic(state), parent)
    while len(opened) != 0 :
        cur = heapq.heappop(opened)
        closed[str(cur[1])] = (cur[2][0],heuristic(cur[1]),cur[3])
        if heuristic(cur[1]) == 0:
            closed[str(cur[1])] = (cur[2][0],cur[2][1],cur[3])
            parent = cur[3]
            path = []
            path.insert(0, cur[1])
            while parent !=[]:
                  path.insert(0, parent)
                  parent = closed[str(parent)][2]
            move = 0
            for i in range(len(path)):
                print(path[i], "h=" + str(heuristic(path[i]))+" moves: "+ str(move))
                move = move + 1
            break;
        state1 = get_succ(cur[1])
        for row in state1:
            if str(row) not in closed:
               heapq.heappush(opened,(cur[2][0]+1+heuristic(row), row, (cur[2][0]+1, heuristic(row), cur[2][2]+1),cur[1]))

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
        
        
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   
                   