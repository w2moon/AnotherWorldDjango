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
    >>> m = mail.sys_add(title,content,attachment)
    >>> m = mail.sys_add(title,content,attachment)
    >>> mail.recieve_sys("13")[0]
    >>> info={'code':'mail_receive','userid':r.userid,}
    >>> ret = do(info)
    """
    ret = dict()
    ret['rc'] = RetCode.OK
    
    mail.recieve_sys(info['userid'])
    ret['mails'] = mail.get_all_mail(info['userid'])
    
    return ret
