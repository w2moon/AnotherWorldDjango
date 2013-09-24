'''
Created on 2013-7-29

@author: pengw
'''
def do(skill,trigger,event_targets,value):
    params = skill.getBase()['param']
    
    targets = skill.getBattleField().select_target(skill.getWarrior().getPlayer(),skill.getWarrior(),params[1],skill.getWarrior().getTraveller().getNature(),True,trigger,event_targets)
    tasks = []
    
    for t in targets:
        tasks.append([t.incHP,[value*params[2]]])
        
    tasks.append([skill.delay,[0.4]])
    
    skill.getBattleField().addTasks(tasks)