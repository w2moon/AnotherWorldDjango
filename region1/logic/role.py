'''
Created on 2013-7-23

@author: pengw
'''
from gameobject import gameobject

class role(gameobject):
    '''
    classdocs
    '''


    def __init__(self,info):
        '''
        Constructor
        '''
        self.info = info
        
    def getUserid(self):
        return self.info['userid']
    
    def getName(self):
        return self.info['name']
    
    def getId(self):
        return self.info['id']
    
    def getLastSeed(self):
        return self.info['lastseed']
    
    def getSlot1(self):
        return self.info['slot1']
    
    def getSlot2(self):
        return self.info['slot2']
    
    def getSlot3(self):
        return self.info['slot3']
    
    def getSlot4(self):
        return self.info['slot4']
    
    def getSlot5(self):
        return self.info['slot5']
    
    def getTraveller(self,tid):
        if tid == 0:
            return None
        for t in self.travellers:
            if t.getId() == tid:
                return t
            
        return None
    
    def getSlotTravellers(self):
        slots = []
        for i in xrange(1,6):
            tid = self.info['slot'+str(i)]
            if tid != 0:
                slots.append(self.getTraveller(tid))
            else:
                slots.append(None)
            
        return slots
        
    
    def getSoul(self,sid):
        if sid == 0:
            return None
        for s in self.souls:
            if s.getId() == sid:
                return s
        
        return None
        