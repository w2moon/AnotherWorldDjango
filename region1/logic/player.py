'''
Created on 2013-7-23

@author: pengw
'''


from gameobject import gameobject
from warrior import warrior
import data
class player(gameobject):
    
    def __init__(self,role,battlefield):
        self.role = role
        self.battlefield = battlefield
        
        self.warriors = []
        travellers = role.getSlotTravellers()
        for v in travellers:
            if v != None:
                self.warriors.append(warrior(self,self.battlefield,v))
            else:
                self.warriors.append(None)
        
        self.hero = self.warriors[data.HERO_IDX]
        
    def isDead(self):
        if self.hero != None:
            return self.hero.isDead()
        for w in self.warriors:
            if w != None and not w.isDead():
                return False
            
        return True
    
    def getWarriors(self):
        return self.warriors
    
    def getHero(self):
        return self.hero
    
        
  
        
        
    
    