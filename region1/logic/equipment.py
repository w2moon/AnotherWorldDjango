'''
Created on 2013-7-24

@author: pengw
'''
from gameobject import gameobject

import data

class equipment(gameobject):
    '''
    classdocs
    '''


    def __init__(self,info):
        '''
        Constructor
        '''
        self.info = info
    
    def getId(self):
        return self.info['id']
    
    def getBaseId(self):
        return self.info['baseid']
    
    def getLevel(self):
        return self.info['level']
    
    def getSkillLevel(self):
        return self.info['skilllevel']
    
    def getBase(self):
        return data.equipmentbase[self.info['baseid']]
    
    def getSkillId(self):
        return self.getBase()['skillid']
    
    def hasSkill(self):
        return self.getBase()['skillid'] != 0