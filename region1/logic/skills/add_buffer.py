'''
Created on 2013-7-29

@author: pengw
'''
def do(skill,trigger,event_targets):
    params = skill.getBase()['param']
    
    tasks = []
    
    tasks.append([skill.delay,[0.01]])
    
    if params[0] == 'eventtarget':
        for t in event_targets:
            tasks.append([t.addBuff,[params[1]]])
            tasks.append([skill.delay,[0.01]])
    else:
        tasks.append([skill.warrior.addBuff,[params[1]]])
        tasks.append([skill.delay,[0.01]])
    
    
    skill.getBattleField().addTasks(tasks)