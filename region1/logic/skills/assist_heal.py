'''
Created on 2013-7-29

@author: pengw
'''
def do(skill,trigger,event_targets):
    
    params = skill.getBase()['param']
    
    targets = skill.getBattleField().select_target(skill.getWarrior().getPlayer(),skill.getWarrior(),params[0],params[1],'lowesthp',True,trigger,event_targets)
    
    tasks = []
    
    tasks.append([skill.delay,[0.4]])
    
    for t in targets:
        tasks.append([skill.getWarrior().heal,[t,params[2],params[3],True]])
        
    tasks.append([skill.delay,[0.4]])
    
    
    skill.getBattleField().addTasks(tasks)