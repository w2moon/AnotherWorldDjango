'''
Created on 2013-7-29

@author: pengw
'''
def do(skill,trigger,event_targets):
    tasks = []
    tasks.append([skill.delay,[0.4]])
    
    tasks.append([skill.getWarrior().moveTo,[trigger]])
    tasks.append([skill.delay,[0.4]])
    
    tasks.append([skill.getWarrior().beGuarder,[trigger]])
    
    skill.getBattleField().addTasks(tasks)