'''
Created on 2013-7-23

@author: pengw
'''
from gameobject import gameobject
import data
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
        
        
        for i in xrange(0,data.EQUIP_NUM):
            if self.info['slot'][i] != 0:
                equip = self.owner.getEquipment(self.info['slot'][i])
                if equip != None :
                    v += equip.getBase()[name]*(equip.getLevel()/equip.getMaxLevel())
                    
                    
        temp = self.getSoul()
        if temp != None:
            v += temp.getBase()[name]*(1+temp.getStar()*0.1)*(temp.getLevel()/temp.getMaxLevel())
        
        if self.info.has_key(name):   
            v += self.info[name]*self.getLevel()
        
        return v
    
    def getSkills(self):
        skills = []
        
        for i in xrange(0,data.EQUIP_NUM):
            if self.info['slot'][i] != 0:
                equip = self.owner.getEquipment(self.info['slot'][i])
                if equip != None and equip.hasSkill():
                    skills.append([equip.getSkillId(),equip.getSkillLevel()])
            
        temp = self.getSoul()
        if temp != None and temp.hasSkill():
            skills.append([temp.getSkillId(),temp.getSkillLevel()])
            
        if self.getSkill1Id() != 0:
            skills.append([self.getSkill1Id(),self.getSkill1Level()])
            
        if self.getSkill2Id() != 0:
            skills.append([self.getSkill2Id(),self.getSkill2Level()])
        
        return skills