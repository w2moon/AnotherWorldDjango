'''
Created on 2013-7-23

@author: pengw
'''
from gameobject import gameobject
from skill import skill
from buff import buff
import wl
import data
class warrior(gameobject):
    def __init__(self,player,battlefield,traveller):
        self.player = player
        self.battlefield = battlefield
        self.traveller = traveller
        
        self.guarder = None
        
        self.hp = 0
        self.maxhp = 0
        self.energy = 0
        self.maxenergy = 0
        
        self.base_property = {}
        self.extra_property = {}
        self.rate_property = {}
        
        self.skills = []
        self.buffs = []
        
        self.disabled = 0
        self.skilldisabled = 0
        
        self.modifier_damage_percent = 0
        
        skills = traveller.getSkills()
        for s in skills:
            self.skills.append(skill(self,battlefield,s[1],data.skillbase[s[0]]))
            
    def notify(self,*args):
        self.battlefield.on_warrior_event(self,*args)
            
    def battle_init(self):
        maxhp = self.traveller.getProperty('MaxHP')
        self.setMaxHP(maxhp)
        self.setHP(maxhp)
        
        maxenergy = 3
        self.setMaxEnergy(maxenergy)
        self.setEnergy(0)
        
        self.notify('battle_init')
        
    def getProperty(self,name):
        v = (self.getBaseProperty(name) + self.getExtraProperty(name))*(1+self.getRateProperty(name))
        if v < 0:
            return 0
        return v
    
    def getBaseProperty(self,name):
        if self.base_property.has_key(name):
            return self.base_property[name] + self.traveller.getProperty(name)
        return self.traveller.getProperty(name)
    
    def incBaseProperty(self,name,v):
        if not self.base_property.has_key(name):
            self.base_property[name] = 0
        self.base_property[name] += v
        
        self.notify('inc'+name,v)
        
    def deccBaseProperty(self,name,v):
        if not self.base_property.has_key(name):
            self.base_property[name] = 0
        self.base_property[name] -= v
        
        self.notify('dec'+name,v)
        
    def getExtraProperty(self,name):
        if self.extra_property.has_key(name):
            return self.extra_property[name]
        return 0
    
    def incExtraProperty(self,name,v):
        if not self.extra_property.has_key(name):
            self.extra_property[name] = 0
        self.extra_property[name] += v
        
        self.notify('incExtra'+name,v)
        
    def decExtraProperty(self,name,v):
        if not self.extra_property.has_key(name):
            self.extra_property[name] = 0
        self.extra_property[name] -= v
        
        self.notify('decExtra'+name,v)
        
    def getRateProperty(self,name):
        if self.extra_property.has_key(name):
            return self.extra_property[name]
        return 0
    
    def incRateProperty(self,name,v):
        if not self.extra_property.has_key(name):
            self.extra_property[name] = 0
        self.extra_property[name] += v
        
        self.notify('incExtra'+name,v)
        
    def decRateProperty(self,name,v):
        if not self.extra_property.has_key(name):
            self.extra_property[name] = 0
        self.extra_property[name] -= v
        
        self.notify('decExtra'+name,v)
        
    def getBattleField(self):
        return self.battlefield
    
    def isEnemy(self,warrior):
        return self.player != warrior.player
    
    def isAlly(self,warrior):
        return self.player == warrior.player
    
    def getPlayer(self):
        return self.player
    
    def getTraveller(self):
        return self.traveller
    
    def setEnergy(self,v):
        self.energy = v
        
    def getEnergy(self):
        return self.energy
    
    def setMaxEnergy(self,v):
        self.maxenergy = v
        
    def getMaxEnergy(self):
        return self.maxenergy
    
    def setHP(self,v):
        self.hp = v
        
    def getHP(self):
        return self.hp
    
    def setMaxHP(self,v):
        self.maxhp = v
        
    def getMaxHP(self):
        return self.maxhp
    
    def incDisabled(self,v):
        self.disabled += v
        
    def decDisabled(self,v):
        self.disabled -= v
        
    def isDisabled(self):
        return self.disabled > 0
    
    def incSkillDisabled(self,v):
        self.skilldisabled += v
        
    def decSkillDisabled(self,v):
        self.skilldisabled -= v
        
    def isSkillDisabled(self):
        return self.skilldisabled > 0
    
    def incModifierDamagePercent(self,v):
        self.modifier_damage_percent += v
        
    def decModifierDamagePercent(self,v):
        self.modifier_damage_percent -= v
        
    def getModifierDamagePercent(self):
        return self.modifier_damage_percent
    
    def rand(self):
        return self.battlefield.rand()
    
    def incHP(self,v):
        isCrit = self.rand() < self.getProperty('Crit')
        if isCrit:
            v *= 2
            
        self.setHP(wl.clamp(self.getHP()+v,0,self.getMaxHP()))
        
        self.notify('incHP',v,isCrit)
        
    def decHP(self,v):
        
        if self.rand() < self.getProperty('Dodge'):
            self.notify('dodge')
            return
        
        isCrit = self.rand() < self.getProperty('Crit')
        if isCrit:
            v *= 2
            
        self.setHP(wl.clamp(self.getHP()-v,0,self.getMaxHP()))
        self.notify('decHP',v,isCrit)
        
        if self.isDead():
            self.dead()
            
    def incMaxHP(self,v):
        self.setMaxHP(self.getMaxHP()+v)
        
        self.notify('incMaxHP',v)
        
    def decMaxHP(self,v):
        self.setMaxHP(wl.clamp(self.getMaxHP()-v, 0, self.getMaxHP()))
        
        self.notify('decMaxHP',v)
        
    def incEnergy(self,v):
        self.setEnergy(wl.clamp(self.getEnergy()+v, 0, self.getMaxEnergy()))
        
        self.notify('incEnergy',v)
        
    def decEnergy(self,v):
        self.setEnergy(wl.clamp(self.getEnergy()-v, 0, self.getMaxEnergy()))
        
        self.notify('decEnergy',v)
        
    def incMaxEnergy(self,v):
        self.setMaxEnergy(self.getMaxEnergy()+v)
        
        self.notify('incMaxEnergy',v)
        
    def decMaxEnergy(self,v):
        self.setMaxEnergy(wl.clamp(self.getMaxEnergy()-v, 0, self.getMaxEnergy()))
        
        self.notify('decMaxEnergy',v)
        
    def beDefender(self,attacker):
        self.notify('beDefender',[attacker])
        
    def setGuarder(self,warrior):
        self.guarder = warrior
        
    def getGuarder(self):
        return self.guarder
    
    def beGuarder(self,warrior):
        warrior.setGuarder(self)
        self.notify('beGuarder',[warrior])
        
    def addBuff(self,buffid,trigger):
        buffinfo = data.buffbase[buffid]
        if buffinfo['multiple'] == 1:
            buffinst = None
            for b in self.buffs:
                if b.getId() == buffid and b.hasLink(trigger):
                    buffinst = b
                    break
                
            if buffinst == None:
                buffinst = buff(self,self.battlefield,buffinfo)
                buffinst.addLink(trigger)
                self.buffs.append(buffinst)
            else:
                if buffinfo.stack > buffinst.stack:
                    buffinst.setStack(buffinst.getStack()+1)
                    
                buffinst.refreshDuration()
                
        else:
            isnew = True
            for b in self.buffs:
                if b.getId() == buffid:
                    b.addLink(trigger)
                    b.refreshDuration()
                    isnew = False
                    break
            if isnew:
                buffinst = buff(self,self.battlefield,buffinfo)
                buffinst.addLink(trigger)
                self.buffs.append(buffinst)
                
    def removeBuff(self,buffid,trigger):
        for b in self.buffs:
            if b.getId() == buffid and b.hasLink(trigger):
                b.removeLink(trigger)
                if b.isCleared():
                    b.destroy()
                    self.buffs.remove(b)
                return
            
    def clearBuffs(self):
        for b in self.buffs:
            b.destroy()
        self.buffs = []
        
    def isDead(self):
        return self.getHP() <= 0
    
    def dead(self):
        self.clearBuffs()
        
        self.notify('dead')
        
    def calc_damage(self,attacker,defenser,protype,prorate):
        damage = attacker.getProperty('Attack') - defenser.getProperty('Defense')
        damage = int(damage*(1+defenser.getModifierDamagePercent()))
        if damage <= 0 :
            damage = 1
        return damage
    
    def calc_heal(self,healer,reciever,protype,prorate):
        v = healer.getProperty('Heal')
        if v < 0:
            v = 0
            
        return v
    
    def canAction(self):
        if self.isDisabled():
            return False
        
        if self.isDead():
            return False
        
        return True
           
    def action(self):
        for s in self.skills:
            if s.isActiveSkill() and s.canBeCast(None,None):
                return s.cast(None,None)
            
    def newturn(self):
        pass
    
    def endturn(self):
        for s in self.skills:
            s.update()
            
        todelete = []
        for b in self.buffs:
            if b.update():
                todelete.append(b)
                 
        for b in todelete:
            self.buffs.remove(b)
            
    def attack(self,target,protype,prorate,nottriggerevent):
        realtarget = target
        if target.getGuarder() != None :
            realtarget = target.getGuarder()
            self.battlefield.addTask(realtarget.moveBack)
            target.setGuarder(None)
        
        damage = self.calc_damage(self, realtarget, protype, prorate)
        realtarget.decHP(damage)
        
        if nottriggerevent != True:
            self.notify('attack',[realtarget])
            
    def defense(self,attacker):
        if self.getGuarder()!=None:
            self.getGuarder().notify('defense',[attacker])
        else:
            self.notify('defense',[attacker])
            
    def heal(self,target,protype,prorate,nottriggerevent):
        realtarget = target
        value = self.calc_heal(self, realtarget, protype, prorate)
        realtarget.incHP(value)
        if nottriggerevent != True:
            self.notify('heal',[realtarget],value)
            
    def moveTo(self,w):
        self.notify('moveTo',w)
        
    def moveBack(self):
        self.notify('moveBack')
        
    def on_event(self,*args):
        tasks = []
        
        for s in self.skills:  
            if not s.isActiveSkill() and s.isListen(args[1]):
                tasks.append([s.on_event,args])
        
        
        self.battlefield.addTasks(tasks)