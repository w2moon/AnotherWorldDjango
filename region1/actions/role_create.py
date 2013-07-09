'''
Created on Apr 21, 2013

@author: w2moon
'''
from django.utils import timezone
from account.models import base

from data.retcode import RetCode

arr = __file__.split('/')
appname = arr[len(arr)-3]

exec("import "+appname)
role = eval("reload("+appname+".models)").role


 

#from region1.models import role

def do(info):
    """
    role create
    >>> info={'code':'role_create','userid':'5','name':'tester','img':''}
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
    >>> info['userid']='5'
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.NAME_EXIST
    True
    """
    ret = dict()
    
    
    obj = role.objects.filter(userid=info['userid'])
    if obj.count() != 0 :
        ret['rc'] = RetCode.PLAYER_EXIST
        return ret
    
    obj = role.objects.filter(name=info['name'])
    if obj.count() != 0 :
        ret['rc'] = RetCode.NAME_EXIST
        return ret
       
    baseinfo = base.objects.filter(userid=info['userid'])
    if baseinfo.count() == 0:
        ret['rc'] = RetCode.USERID_NOTEXIST
        return ret
    else:
        baseinfo = baseinfo[0]
        
    obj = role(id=baseinfo.id,userid=info['userid'],name=info['name'],date_lastupdate=timezone.now(),date_lastenter=timezone.now(),date_create=timezone.now())
    
    obj.hp = 10
    obj.exp = 0
    obj.level = 1
    obj.copper = 0
    obj.gold = 0
    
    obj.extrasoulnum = 0
    obj.extraequipmentnum = 0
    obj.extratravellernum = 0
    
    obj.save()
    

    ret['rc'] = RetCode.OK
    ret['player'] = obj.packforself()
    return ret