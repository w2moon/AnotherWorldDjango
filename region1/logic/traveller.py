'''
Created on 2013-7-23

@author: pengw
'''
from gameobject import gameobject

class traveller(gameobject):
    def __init__(self,info,owner):
        self.info = info
        
        self.owner = owner
        
    def getId(self):
        return self.info['id']
    
    def getName(self):
        return self.info['name']
    
    def getLevel(self):
        return self.info['level']
        
    def getNature(self):
        return self.info['nature']
        
    def getSoulId(self):
        return self.info['soulid']
        
    def getSoul(self):
        return self.owner.getSoul(self.getSoulId())
    
    def getSkill1Id(self):
        return self.info['skill1id']
    
    def getSkill1Level(self):
        return self.info['skill1level']
    
    def getSkill2Id(self):
        return self.info['skill2id']
    
    def getSkill2Level(self):
        return self.info['skill2level']
    
    def getWeaponId(self):
        return self.info['weaponid']
    
    def getClothId(self):
        return self.info['clothid']
    
    def getTrinketId(self):
        return self.info['trinketid']
    
    def getWeapon(self):
        return self.owner.getEquipment(self.getWeaponId())
    
    def getCloth(self):
        return self.owner.getEquipment(self.getClothId())
    
    def getTrinket(self):
        return self.owner.getEquipment(self.getTrinketId())
    
    def getProperty(self,name):
        v = 0
        
        temp = self.getWeapon()
        if temp != None:
            v += temp.getBase()[name]
        temp = self.getCloth()
        if temp != None:
            v += temp.getBase()[name]
        temp = self.getTrinket()
        if temp != None:
            v += temp.getBase()[name]
        temp = self.getSoul()
        if temp != None:
            v += temp.getBase()[name]
        
        if self.info.has_key(name):   
            v += self.info[name]
        
        return v
    
    def getSkills(self):
        skills = []
        
        temp = self.getWeapon()
        if temp != None and temp.hasSkill():
            skills.push([temp.getSkillId(),temp.getSkillLevel()])
            
        temp = self.getCloth()
        if temp != None and temp.hasSkill():
            skills.push([temp.getSkillId(),temp.getSkillLevel()])
            
        temp = self.getTrinket()
        if temp != None and temp.hasSkill():
            skills.push([temp.getSkillId(),temp.getSkillLevel()])
            
        temp = self.getSoul()
        if temp != None and temp.hasSkill():
            skills.push([temp.getSkillId(),temp.getSkillLevel()])
        
        return skills