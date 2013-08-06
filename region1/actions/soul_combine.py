'''
Created on Apr 21, 2013

@author: w2moon
'''

from data.retcode import RetCode
import data
import wl

arr = __file__.split('/')
appname = arr[len(arr)-3]
utils = None
exec("from "+appname+" import utils")

def do(info):
    """
    soul combine
    >>> info={'code':'soul_combine','userid':'1','blueprint':'1'}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.OK
    True
    """
    ret = dict()
    
    role = utils.get_role(info['userid'])
    if role == None :
        ret['rc'] = RetCode.USERID_NOTEXIST
        return ret
    
    
    ret['rc'] = RetCode.OK
    return ret
