'''
Created on 2013-7-29

@author: pengw
'''
def do(skill,trigger,event_targets):
    params = skill.getBase()['param']
    
    targets = skill.getBattleField().select_target(skill.getWarrior().getPlayer(),skill.getWarrior(),'enemy',params[0],skill.warrior.getTraveller().getNature(),True,trigger,event_targets)
    
    tasks = []
    
        