'''
Created on 2013-7-24

@author: pengw
'''

from gameobject import gameobject

import data

class soul(gameobject):
    '''
    classdocs
    '''


    def __init__(self,info):
        '''
        Constructor
        '''
        self.info = info
        self.base = data.soulbase[self.getBaseId()]
        
    def getId(self):
        return self.info['id']
    
    def getBaseId(self):
        return self.info['baseid']
    
    def getLevel(self):
        return self.info['level']
    
    def setLevel(self,v):
        self.info['level'] = v
        
    def getMaxLevel(self):
        return data.rarityclass[self.base['rarityclass']]['maxlevel']
        
    def getSkillLevel(self):
        return self.info['skilllevel']
    
    def setSkillLevel(self,v):
        self.info['skilllevel'] = v
        
    def getStar(self):
        return self.info['star']
    
    def setStar(self,v):
        self.info['star'] = v
        
    def getBase(self):
        return self.base
    
    def getSkillId(self):
        return self.base['skillid']
    
    def hasSkill(self):
        return self.base['skillid'] != 0
    
    
        
    