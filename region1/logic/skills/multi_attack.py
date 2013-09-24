'''
Created on 2013-7-29

@author: pengw
'''
def do(skill,trigger,event_targets):
    params = skill.getBase()['param']
    
    targets = skill.getBattleField().select_target(skill.getWarrior().getPlayer(),skill.getWarrior(),params[0],params[1],5,True,trigger,event_targets)
    
    tasks = []
    
    if len(params) >= 5:
        tasks.append([skill.delay,[0.4]])
        
    lastt = None
    for t in targets:
        if lastt != t:
            lastt = t
            tasks.append([skill.getWarrior().moveTo,[t]])
            tasks.append([skill.delay,[0.4]])
        
        tasks.append([t.beDefender,[skill.getWarrior()]])
        tasks.append([skill.delay,[0.01]])
        
        tasks.append([t.defense,[skill.getWarrior()]])
        tasks.append([skill.delay,[0.01]])
        
        tasks.append([skill.getWarrior().attack,[t,params[2],params[3],False]])
        tasks.append([skill.delay,[0.4]])
        
    tasks.append([skill.getWarrior().incEnergy,[1]])
    
    tasks.append([skill.getWarrior().moveBack,[]])
    tasks.append([skill.delay,[0.4]])
    
    skill.getBattleField().addTasks(tasks)