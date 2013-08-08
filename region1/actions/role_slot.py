'''
Created on Apr 21, 2013

@author: w2moon
'''

from data.retcode import RetCode
import data

arr = __file__.split('/')
appname = arr[len(arr)-3]
utils = None
exec("from "+appname+" import utils")

def do(info):
    """
    role slot
    >>> import wl
    >>> r = utils.create_role('10','10','tester')
    >>> r.save()
    >>> tinfo={'userid':'10','name':'traveller','gender':0,'age':0,'img':'','ishuman':1}
    >>> travellerbase = wl.get_rand(data.travellerbase)
    >>> t = r.addTraveller(tinfo,travellerbase)
    >>> info={'code':'role_slot','userid':'10','slot':1,'traveller':t.id}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.OK
    True
    >>> role = utils.get_role(info['userid'])
    >>> role.slot1 == t.id
    True
    >>> info['traveller'] = 0
    >>> ret = do(info)
    >>> role = utils.get_role(info['userid'])
    >>> role.slot1 == 0
    True
    >>> role.slot5 = t.id
    >>> role.save()
    >>> info['slot']=5
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.CAN_NOT_CHANGE_HERO
    True
    """
    ret = dict()
    ret['rc'] = RetCode.OK
    
    role = utils.get_role(info['userid'])
    if role == None :
        ret['rc'] = RetCode.USERID_NOTEXIST
        return ret
    
    if data.HERO_IDX+1 == info['slot']:
        ret['rc'] = RetCode.CAN_NOT_CHANGE_HERO
        return ret
    
    if info['traveller'] != 0:
        t = role.getTraveller(info['traveller'])
        if t == None:
            ret['rc'] = RetCode.TRAVELLER_NOTEXIST
            return ret
    
    if getattr(role,'slot'+str(info['slot'])) == info['traveller']:
        return ret
    
    setattr(role,'slot'+str(info['slot']),info['traveller'])
    role.save()
    
    return ret
