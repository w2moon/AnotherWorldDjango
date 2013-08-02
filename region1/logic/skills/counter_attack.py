'''
Created on 2013-7-29

@author: pengw
'''
def do(skill,trigger,event_targets):
    tasks = []
    
    params = skill.getBase().param
    targets = event_targets
    
    tasks.append([skill.delay,[0.4]])
    
    for t in targets:
        
        tasks.append([t.defense,[skill.getWarrior()]])
        tasks.append([skill.delay,[0.01]])
        
        tasks.append([skill.getWarrior().attack,[t,params[0],params[1],True]])
        tasks.append([skill.delay,[0.4]])
        
        break
    
    skill.getBattleField().addTasks(tasks)