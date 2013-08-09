'''
Created on Apr 21, 2013

@author: w2moon
'''

from data.retcode import RetCode

import mail

arr = __file__.split('/')
appname = arr[len(arr)-3]
utils = None
exec("from "+appname+" import utils")

def do(info):
    """
    mail send
    >>> r = utils.create_role('14','14','tester')
    >>> r.save()
    >>> m = mail.user_send("hi","content","",0,"",r.userid)
    >>> info={'code':'mail_send','userid':r.userid,'mailid':m.id}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.OK
    True
    """
    ret = dict()
    ret['rc'] = RetCode.OK
    
   
    
    return ret
