'''
Created on Apr 21, 2013

@author: w2moon
'''
from django.utils import timezone


from data.retcode import RetCode

arr = __file__.split('/')
appname = arr[len(arr)-3]
utils = None
exec("from "+appname+" import utils")


 

#from region1.models import role

def do(info):
    """
    region enter test
    >>> info={'code':'region_enter','userid':'1','data':'check'}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.PLAYER_NOTEXIST
    True
    >>> r = utils.create_role('1','1','tester')
    >>> r.save()
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.OK
    True
    >>> r.delete()
    """
    ret = dict()
    obj = utils.get_role(info['userid'])
    if obj == None :
        ret['rc'] = RetCode.PLAYER_NOTEXIST
        return ret
          
    obj.date_lastenter = timezone.now()
    obj.save()
    
    obj.new_randstate()
    
    ret['rc'] = RetCode.OK
    ret['player'] = obj.packforself()
    return ret