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
    >>> r2 = utils.create_role('15','15','tester')
    >>> r2.save()
    >>> info={'code':'mail_send','userid':r.userid,'title':'title','content':'content','touser':r2.userid,'todeveloper':0}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.OK
    True
    >>> mail.recieve_sys(r2.userid)
    >>> m = mail.get_all_mail(r2.userid)[0]
    >>> m['issys'] == 0L
    True
    >>> m['sender_userid'] == r.userid
    True
    >>> num = mail.get_mail_num(r2.userid)
    >>> info['todeveloper'] = 1
    >>> ret = do(info)
    >>> num == mail.get_mail_num(r2.userid)
    True
    """
    ret = dict()
    ret['rc'] = RetCode.OK
    
    sender = utils.get_role(info['userid'])
    
    if info['todeveloper'] == 1:
        mail.developer_send(info['title'], info['content'], "", info['userid'], sender.name)
    else:
        reciever = utils.get_role(info['touser'])
        
        if sender == None or reciever == None or sender == reciever:
            ret['rc'] = RetCode.PLAYER_NOTEXIST
        else:
            mail.user_send(info['title'], info['content'], "", info['userid'], sender.name, info['touser'])
    
    
    return ret
