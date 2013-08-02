'''
Created on 2013-7-23

@author: pengw
'''


from gameobject import gameobject
from warrior import warrior

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
        
        self.hero = self.warriors[0]
        
    def isDead(self):
        return self.hero.isDead()
    
    def getWarriors(self):
        return self.warriors
    
    def getHero(self):
        return self.hero
    
        
  
        
        
    
    