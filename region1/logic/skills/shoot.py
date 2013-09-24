'''
Created on 2013-7-29

@author: pengw
'''
def do(skill,trigger,event_targets):
    params = skill.getBase()['param']
    
    targets = skill.getBattleField().select_target(skill.getWarrior().getPlayer(),skill.getWarrior(),'enemy',params[1],params[0],True,trigger,event_targets)
    
    tasks = []
    
    for t in targets:
        tasks.append([t.beDefender,[skill.getWarrior()]])
        tasks.append([skill.delay,[0.01]])
        
        tasks.append([t.defense,[skill.getWarrior()]])
        tasks.append([skill.delay,[0.01]])
        
        tasks.append([skill.getWarrior().attack,[t,params[6],params[7],False]])
        tasks.append([skill.delay,[0.4]])