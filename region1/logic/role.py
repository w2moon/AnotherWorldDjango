'''
Created on 2013-7-23

@author: pengw
'''
from gameobject import gameobject

import wl
import data

from traveller import traveller
from soul import soul
from equipment import equipment

class role(gameobject):
    '''
    classdocs
    '''
    def create_enemy(tmp,idx,factor,eid,elevel):
        einfo = data.enemy[eid]
        traveller = {
                        'id':wl.local_id(),
                        'level':elevel*factor,
                        'skill1id':einfo['skill1id'],
                        'skill1level':einfo['skill1level']*factor,
                        'skill2id':einfo['skill2id'],
                        'skill2level':einfo['skill2level']*factor,
                        'nature':4,
                        'soulid':0,
                        'MaxHP':einfo['MaxHP']*factor,
                        'Attack':einfo['Attack']*factor,
                        'Defense':einfo['Defense']*factor,
                        'Heal':einfo['Heal']*factor,
                        'slot':[0,0,0,0],
                     }
        tmp['slot'+str(idx)] = traveller['id']
        if einfo['soulid'] != 0:
            soul = {
                        'id':wl.local_id(),
                        'baseid':einfo['soulid'],
                        'star':einfo['soulstar'],
                        'level':einfo['soullevel']*factor,
                        'skilllevel':einfo['soulskilllevel']*factor,
                    }
            tmp['souls'].append(soul)
            traveller['soulid'] = soul['id']
        else:
            traveller['soulid'] = 0
            
        if einfo['weaponrid'] != 0:
            weaponr = {
                        'id':wl.local_id(),
                        'baseid':einfo['weaponrid'],
                        'level':einfo['weaponrlevel']*factor,
                        'skilllevel':einfo['weaponrskilllevel']*factor,
                    }
            tmp['equipments'].append(weaponr)
            traveller['slot'][data.EQUIP_WEAPONR] = weaponr['id']
        else:
            traveller['slot'][data.EQUIP_WEAPONR]  = 0
            
        if einfo['weaponlid'] != 0:
            weaponl = {
                        'id':wl.local_id(),
                        'baseid':einfo['weaponlid'],
                        'level':einfo['weaponllevel']*factor,
                        'skilllevel':einfo['weaponlskilllevel']*factor,
                    }
            tmp['equipments'].append(weaponl)
            traveller['slot'][data.EQUIP_WEAPONL] = weaponl['id']
        else:
            traveller['slot'][data.EQUIP_WEAPONL]  = 0
            
        if einfo['clothid'] != 0:
            cloth = {
                        'id':wl.local_id(),
                        'baseid':einfo['clothid'],
                        'level':einfo['clothlevel']*factor,
                        'skilllevel':einfo['clothskilllevel']*factor,
                    }
            tmp['equipments'].append(cloth)
            traveller['slot'][data.EQUIP_CLOTH] = soul['id']
        else:
            traveller['slot'][data.EQUIP_CLOTH] = 0
            
        if einfo['trinketid'] != 0:
            trinket = {
                        'id':wl.local_id(),
                        'baseid':einfo['trinketid'],
                        'level':einfo['trinketlevel']*factor,
                        'skilllevel':einfo['trinketskilllevel']*factor,
                    }
            tmp['equipments'].append(trinket)
            traveller['slot'][data.EQUIP_TRINKET] = soul['id']
        else:
            traveller['slot'][data.EQUIP_TRINKET] = 0
            
        tmp['travellers'].append(traveller)
        
    def create_from_enemy(enemies,level,heros):
        local_id = wl.local_id()
        tmp = {
               'id':local_id,
               'userid':str(local_id),
               'travellers':[],
               'souls':[],
               'equipments':[],
               }
        
        idx = 0
        factor = level
        for e in enemies:
            idx += 1
            if e[0] == 0:
                tmp['slot'+str(idx)] = 0
                continue
            role.create_enemy(tmp,idx,factor,e[0],e[1])
            
        for i in xrange(idx+1,6):
            tmp['slot'+str(i)] = 0
            
        for e in heros:
            if e[0] != 0:
                role.create_enemy(tmp,data.HERO_IDX,factor,e[0],e[1])
            
        return role(tmp)
                
            
    create_enemy = staticmethod(create_enemy)
    create_from_enemy = staticmethod(create_from_enemy)


    def __init__(self,info):
        '''
        Constructor
        '''
        self.info = info
        
        self.travellers = []
        self.souls = []
        self.equipments = []
        
        for t in self.info['travellers']:
            self.travellers.append(traveller(t,self))
            
        for t in self.info['souls']:
            self.souls.append(soul(t))
            
        for t in self.info['equipments']:
            self.equipments.append(equipment(t))
        
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
    
    def getEquipment(self,sid):
        if sid == 0:
            return None
        for s in self.equipments:
            if s.getId() == sid:
                return s
        
        return None
        