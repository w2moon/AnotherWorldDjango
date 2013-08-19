'''
Created on Apr 21, 2013

@author: w2moon
'''

import data

from data.retcode import RetCode

arr = __file__.split('/')
appname = arr[len(arr)-3]
utils = None
exec("from "+appname+" import utils")

 

#from region1.models import role

def do(info):
    """
    role create
    >>> info={'code':'role_create','userid':'5','name':'tester'}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.USERID_NOTEXIST
    True
    >>> info['userid']='1'
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.OK
    True
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.PLAYER_EXIST
    True
    >>> role = utils.get_role(1)
    >>> role == None
    False
    >>> randstate = role.get_randstate()
    >>> s = randstate.seed("asd")
    >>> randstate.save()
    >>> randstate.rand()
    0.8907628381841943
    >>> randstate.rand()
    0.6904938114977092
    >>> randstate.reset()
    >>> randstate.rand()
    0.8907628381841943
    >>> randstate.rand()
    0.6904938114977092
    """
    ret = dict()
    
    baseinfo = utils.get_account(info['userid']) 
    if baseinfo == None:
        ret['rc'] = RetCode.USERID_NOTEXIST
        return ret
    
    obj = utils.get_role(info['userid']) 
    if obj != None :
        ret['rc'] = RetCode.PLAYER_EXIST
        return ret
        
    obj = utils.create_role(baseinfo.id,info['userid'],info['name']) 
    
    rolecfg = data.get_rolecfg()  
    obj.hp = rolecfg['initMaxHP']
    obj.exp = 0
    obj.level = rolecfg['initLevel']
    obj.copper = rolecfg['initCopper']
    obj.gold = rolecfg['initGold']
    
    obj.extrasoulnum = 0
    obj.extraequipmentnum = 0
    obj.extratravellernum = 0
    
    obj.save()
    
    obj.new_randstate()
    

    ret['rc'] = RetCode.OK
    ret['player'] = obj.packforself()
    return ret