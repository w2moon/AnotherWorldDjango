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
    soul starup
    >>> r = utils.create_role('7','7','tester')
    >>> r.addCopper(10000)
    >>> s1 = r.addSoul(1)
    >>> s2 = r.addSoul(2)
    >>> s3 = r.addSoul(1)
    >>> r.save()
    >>> info={'code':'soul_starup','userid':'7','soulid1':'1','soulid2':'2'}
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
