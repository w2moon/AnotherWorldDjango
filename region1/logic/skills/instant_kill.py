'''
Created on 2013-7-29

@author: pengw
'''
def do(skill,trigger,event_targets):
    params = skill.getBase().param
    targets = event_targets
    
    tasks = []
    
    for t in targets:
        tokill = False
        
        if params[0] == 'hppercent':
            if t.getHP()*0.1/t.getMaxHP() <= params[1]:
                tokill = True
                
        if not tokill:
            continue
        
        tasks.append([skill.delay,[0.4]])
        
        tasks.append([t.decHP,[t.getHP()]])
        tasks.append([skill.delay,[0.01]])
        
    skill.getBattleField().addTasks(tasks)