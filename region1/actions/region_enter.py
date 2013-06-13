'''
Created on Apr 21, 2013

@author: w2moon
'''
from django.utils import timezone


from data.retcode import RetCode

arr = __file__.split('/')
appname = arr[len(arr)-3]

exec("import "+appname)
role = eval("reload("+appname+".models)").role


 

#from region1.models import role

def do(info):
    """
    region enter test
    >>> info={'code':'region_enter','userid':'1','data':'check'}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.PLAYER_NOTEXIST
    True
    >>> r = role(id='1',userid='1',name='tester',date_lastupdate=timezone.now(),date_lastenter=timezone.now(),date_create=timezone.now())
    >>> r.save()
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.OK
    True
    >>> r.delete()
    """
    ret = dict()
    obj = role.objects.filter(userid=info['userid'])
    if obj.count() == 0 :
        ret['rc'] = RetCode.PLAYER_NOTEXIST
        return ret
    else:
        obj = obj[0]
       
       
    obj.date_lastenter = timezone.now()
    obj.save()
    

    ret['rc'] = RetCode.OK
    ret['player'] = obj.packforself()
    return ret