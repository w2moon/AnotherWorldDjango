'''
Created on Apr 21, 2013

@author: w2moon
'''
from django.utils import timezone


from data.retcode import RetCode

import wl
import data

arr = __file__.split('/')
appname = arr[len(arr)-3]
utils = None
exec("from "+appname+" import utils")


 
#from region1.models import role

def do(info):
    """
    battle stage test
    >>> r = utils.create_role('2','2','tester')
    >>> r.save()
    >>> info={'code':'battle_stage','userid':'2','stage_id':1001,'level':1,'submap':1}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.BATTLE_NOTHAVEHERO
    True
    >>> tinfo={'userid':'2','name':'traveller','gender':0,'age':0,'img':'tester'}
    >>> travellerbase = wl.get_rand(data.travellerbase)
    >>> t = r.addTraveller(tinfo,travellerbase)
    >>> t.skill2id = 1202
    >>> t.save()
    >>> r.equipTraveller("slot1",t.id)
    >>> tinfo={'userid':'2','name':'traveller','gender':0,'age':0,'img':'tester'}
    >>> travellerbase = wl.get_rand(data.travellerbase)
    >>> t = r.addTraveller(tinfo,travellerbase)
    >>> t.skill2id = 2000
    >>> t.save()
    >>> r.equipTraveller("slot2",t.id)
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.BATTLE_LOW_HP
    True
    >>> r.hp = 10
    >>> r.save()
    >>> ret = do(info)
    >>> ret['rc'] != RetCode.BATTLE_LOW_HP
    True
    """
    ret = dict()
    
    ret['rc'] = utils.battle_pve(info)
    if ret['rc'] == RetCode.BATTLE_RESULT_WIN:
        role = utils.get_role(info['userid'])
        ret['reward'] = role.addReward(data.stage[info['stage_id']]['reward'],info['level'])
        completestate = role.completeStage(info['stage_id'],info['level'])
        if  completestate == role.COMPLETE_FIRST:
            rewardfirst = role.addReward(data.stage[info['stage_id']]['rewardfirst'],info['level'])
            ret['reward'] = wl.dict_merge(ret['reward'],rewardfirst)
        
        if  completestate == role.COMPLETE_FIRST or completestate == role.COMPLETE_LEVEL:
            completemap = True
            submapinfo = data.submaps[info['submap']]
            for stageid in submapinfo['stages']:
                if not role.isCompleteStage(stageid,info['level']):
                    completemap = False
                    break
                
            if completemap:
                trinket = None
                if  completestate == role.COMPLETE_FIRST:
                    trinket = role.addEquip(submapinfo['trinket'])
                else:
                    trinket = role.findEquip(submapinfo['trinket'])
                    
                trinket.level = info['level']
                trinket.save()
                
                ret['trinket'] = trinket.pack()
                
        role.save()
    else:
        ret['reward'] = {}
    
    
    return ret