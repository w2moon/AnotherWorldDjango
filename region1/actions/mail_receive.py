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
    mail receive
    >>> r = utils.create_role('13','13','tester')
    >>> r.save()
    >>> title = "hi"
    >>> content = "content"
    >>> attachment = ""
    >>> m1 = mail.sys_add(title,content,attachment)
    >>> m2 = mail.sys_add(title,content,attachment)
    >>> info={'code':'mail_receive','userid':r.userid,}
    >>> ret = do(info)
    >>> len(ret['mails']) == 2
    True
    >>> ret = do(info)
    >>> len(ret['mails']) == 2
    True
    """
    ret = dict()
    ret['rc'] = RetCode.OK
    
    mail.recieve_sys(info['userid'])
    ret['mails'] = mail.get_all_mail(info['userid'])
    
    return ret
