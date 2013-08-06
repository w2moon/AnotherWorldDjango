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
    equip make
    >>> r = utils.create_role('6','6','tester')
    >>> r.addCopper(100)
    >>> r.save()
    >>> info={'code':'equip_make','userid':'6','blueprint':'1'}
    >>> mat = r.addMaterial(1,5)
    >>> prn = r.addBlueprint(1)
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.OK
    True
    >>> ret.has_key('equip')
    True
    """
    ret = dict()
    
    role = utils.get_role(info['userid'])
    if role == None :
        ret['rc'] = RetCode.USERID_NOTEXIST
        return ret
    
    equip = role.composeBlueprint(info['blueprint'])
    
    ret['rc'] = RetCode.OK
    
    if equip != None:
        ret['equip'] = equip.pack()
        
    return ret
