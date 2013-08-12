'''
Created on Apr 21, 2013

@author: w2moon
'''

from data.retcode import RetCode

import mail
import wl
arr = __file__.split('/')
appname = arr[len(arr)-3]
utils = None
exec("from "+appname+" import utils")

def do(info):
    """
    mail read
    >>> r = utils.create_role('12','12','tester')
    >>> r.save()
    >>> m = mail.user_send("hi","content","",0,"",r.userid)
    >>> info={'code':'mail_read','userid':r.userid,'mailid':m.id}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.OK
    True
    >>> m = mail.get_mail(info['mailid'])
    >>> m.status == 1
    True
    """
    ret = dict()
    ret['rc'] = RetCode.OK
    
    m = mail.get_mail(info['mailid'])
    if not m.isReaded():  
        if m.attachment != "":
            role = utils.get_role(info['userid'])
            reward = {'attachment':m.attachment}
            wl.csv_param(reward,[ ['attachment',[";",","]] ])
            ret['reward'] = role.addReward(reward['attachment'])
            role.save()
        m.read()
    
    return ret
