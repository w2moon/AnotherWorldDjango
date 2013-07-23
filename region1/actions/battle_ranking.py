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


 

def do(info):
    """
    battle stage test
    >>> info={'code':'battle_ranking','userid':'1','rank':'1','role_id':'1'}
    >>> ret = do(info)
    """