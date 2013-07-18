'''
Created on Apr 21, 2013

@author: w2moon
'''
from django.utils import timezone


from data.retcode import RetCode

import wl

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
    role = utils.get_role(info['userid'])
    if role == None :
        ret['rc'] = RetCode.PLAYER_NOTEXIST
        return ret
    
    timecur = timezone.now()
    distance_day = wl.timezone_day_distance(timecur,role.date_lastenter)
    if distance_day >= 1:
        role.new_randstate()
        
    if distance_day == 1:
        role.checkin_num = role.checkin_num + 1
    
    if timecur.year != role.date_lastenter.year and timecur.month != role.date_lastenter.month:
        role.checkin_num = 0
    
    role.date_lastenter = timecur
    role.save()
    
    
    ret['rc'] = RetCode.OK
    ret['player'] = role.packforself()
    return ret