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
                self.warriors.index(warrior(v))
        
        self.hero = self.warriors[0]
        
    def isDead(self):
        return self.hero.isDead()
    
    def getWarriors(self):
        return self.warriors
        
  
        
        
    
    