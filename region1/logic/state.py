'''
Created on 2013-7-26

@author: pengw
'''

import data



def state_normal(s):
    s.state = state_start
    return data.ACTION_INTERVAL

def state_start(s):
    s.turn = 1
    s.state = state_newturn
    return 0

def state_newturn(s):
    if s.turn > data.MAX_BATTLE_TURN:
        s.result = False
        s.state = state_finish
        return 0
    
    s.idx_acting = 0
    s.state = state_action
    
    for w in s.getWarriors():
        w.newturn()
        
    return 0

def state_finish(s):
    return data.ACTION_INTERVAL

def state_action(s):
    dt = 0
    warriors = s.getWarriors()
    if s.idx_acting < len(warriors):
        if warriors[s.idx_acting].canAction():
            dt = warriors[s.idx_acting].action()
            
            
        s.idx_acting += 1
        
        while s.idx_acting < len(warriors) and (warriors[s.idx_acting] == None or warriors[s.idx_acting].isDead()):
            s.idx_acting += 1
    else:
        for p in s.players:
            if p.isDead():
                s.result = s.players[0] != p
                s.state = state_finish
                return 0
        s.state = state_endturn
        
    return dt

def state_endturn(s):
    for w in s.getWarriors():
        w.endturn()
        
    s.state = state_newturn
    s.turn += 1
    return data.ACTION_INTERVAL