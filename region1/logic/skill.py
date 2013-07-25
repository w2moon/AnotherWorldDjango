'''
Created on 2013-7-24

@author: pengw
'''
from gameobject import gameobject
import skills

class skill(gameobject):
    
    def __init__(self,warrior,battlefield,level,skillbase):
        self.level = level
        self.skillbase = skillbase
        self.warrior = warrior
        self.battlefield = battlefield
        self.cooldown = 0
        
    def battle_init(self):
        self.cooldown = 0
        
    def on_event(self,warrior,event,event_targets,*fargs):
        if self.skillbase.event_id != event:
            return
        
        if (self.skillbase.event_trigger == 'ally_except_me' or self.skillbase.event_trigger == 'all_except_me') and self.warrior == warrior:
            return
        elif self.skillbase.event_trigger == 'self' and self.warrior != warrior:
            return
        elif (self.skillbase.event_trigger == 'enemy' and not self.warrior.isEnemy(warrior)) or (self.skillbase.event_trigger != 'enemy' and self.warrior.isEnemy(warrior)):
            return
        
        if not self.canBeCast(warrior,event_targets):
            return
        
        args = (warrior,event_targets)+fargs
        
        return self.cast(*args)
    
    def getBase(self):
        return self.skillbase
    
    def getBattleFiled(self):
        return self.battlefield
    
    def getNeedEnergy(self):
        return self.skillbase.energy
    
    def getCoolDown(self):
        return self.cooldown
    
    def setCoolDown(self,v):
        self.cooldown = v
        
    def startCoolDown(self):
        self.cooldown = self.skillbase.cooldown
        
    def update(self):
        self.cooldown -= 1
        if self.cooldown < 0:
            self.cooldown = 0
            
    def canBeCast(self,trigger,event_targets):
        if self.warrior.rand() > self.getBase()['max_cast_rate']:
            return False
        
        if not self.isActiveSkill() and self.warrior.isSkillDisabled():
            return False
        
        if self.warrior.getEnergy() < self.getBase()['energy']:
            return False
        
        if self.cooldown != 0:
            return False
        
        if self.getBase()['condition'] != '':
            for v in self.getBase()['condition']:
                if v[0] != "" and not self.isTargetValid(v[0],v[2],v[1] == 'alive',trigger,event_targets):
                    return False
            
        return True
    
    def isTargetValid(self,typ,num,needalive,trigger,event_targets):
        if typ == "none":
            return True
        
        targets = self.battlefield.select_target(self.warrior.getPlayer(),self.warrior,typ,num,self.warrior.getTraveller().getNature(),needalive,trigger,event_targets)
        
        return len(targets) > 0
    
    def cast(self,trigger,event_targets,*args):
        if self.getBase()['energy'] != 0:
            self.warrior.decEnergy(self.getBase()['energy'])
            
        self.startCoolDown()
        
        skills[self.getBase()['action']](self,trigger,event_targets,*args)
            
        return self.getBase()['duration']
    
    def target_take_effect(self,typ,num,needalive,action,particle,effecttype,effectvalue,trigger,event_targets):
        if typ == "none":
            return
        
    def isActiveSkill(self):
        return self.skillbase.event_id == "action"
    