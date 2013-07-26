'''
Created on 2013-7-23

@author: pengw
'''
from gameobject import gameobject

import wl
import data

class role(gameobject):
    '''
    classdocs
    '''
    def create_from_enemy(enemies):
        local_id = wl.local_id()
        tmp = {
               'id':local_id,
               'userid':str(local_id),
               'travellers':[],
               'souls':[],
               'equipments':[],
               }
        
        for e in enemies:
            einfo = data.enemy[e[0]]
            traveller = {
                            'id':wl.local_id(),
                            'level':e[1],
                            'skill1id':einfo.skill1id,
                            'skill1level':einfo.skill1level,
                            'skill2id':einfo.skill2id,
                            'skill2level':einfo.skill2level,
                            'nature':4,
                         }
            
            if einfo.soulid != 0:
                soul = {
                            'id':wl.local_id(),
                            'baseid':einfo.soulid,
                            'level':einfo.soullevel,
                            'skilllevel':einfo.skilllevel,
                        }
                tmp['souls'].append(soul)
                traveller['soulid'] = soul['id']
            else:
                traveller['soulid'] = 0
                
            if einfo.weaponid != 0:
                weapon = {
                            'id':wl.local_id(),
                            'baseid':einfo.weaponid,
                            'level':einfo.weaponlevel,
                            'skilllevel':einfo.weaponskilllevel,
                        }
                tmp['equipments'].append(weapon)
                traveller['weaponid'] = weapon['id']
            else:
                traveller['weaponid'] = 0
                
            if einfo.clothid != 0:
                cloth = {
                            'id':wl.local_id(),
                            'baseid':einfo.clothid,
                            'level':einfo.clothlevel,
                            'skilllevel':einfo.clothskilllevel,
                        }
                tmp['equipments'].append(cloth)
                traveller['clothid'] = soul['id']
            else:
                traveller['soulid'] = 0
                
            if einfo.trinketid != 0:
                trinket = {
                            'id':wl.local_id(),
                            'baseid':einfo.trinketid,
                            'level':einfo.trinketlevel,
                            'skilllevel':einfo.trinketskilllevel,
                        }
                tmp['equipments'].append(trinket)
                traveller['trinketid'] = soul['id']
            else:
                traveller['trinketid'] = 0
                
            tmp['travellers'].append(traveller)
            
        return role(tmp)
                
            
    create_from_enemy = staticmethod(create_from_enemy)


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
        