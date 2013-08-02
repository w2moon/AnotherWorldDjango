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
    >>> info={'code':'battle_stage','userid':'2','stage_id':1001}
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
        ret['reward'] = role.addReward(data.stage[info['stage_id']]['reward'])
        
        role.save()
    else:
        ret['reward'] = {}
    
    
    return ret