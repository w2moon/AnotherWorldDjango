'''
Created on 2013-7-29

@author: pengw
'''
def do(skill,trigger,event_targets):
    params = skill.getBase().param
    targets = event_targets
    
    tasks = []
    
    tasks.append([skill.delay,[0.4]])
    
    for t in targets:
        tasks.append([skill.getWarrior().moveTo,[t]])
        tasks.append([skill.delay,[0.4]])
        
        tasks.append([t.defense,[skill.getWarrior()]])
        tasks.append([skill.delay,[0.01]])
        
        tasks.append([skill.getWarrior().attack,[t,params[0],params[1],True]])
        tasks.append([skill.delay,[0.4]])
        
        break
    
    tasks.append([skill.getWarrior().moveBack,[]])
    tasks.append([skill.delay,[0.4]])
    
    skill.getBattleField().addTasks(tasks)