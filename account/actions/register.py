'''
Created on Apr 21, 2013

@author: w2moon
'''
from django.utils import timezone

from account.models import base
from retcode import RetCode

def do(info):
        """
        register test
        >>> info={'userid':'2','pwd':'123','name':'tester','ip':'127.0.0.1'}
        >>> ret = do(info)
        >>> ret['rc'] == RetCode.NAME_EXIST
        True
        >>> info['userid'] = '1';
        >>> ret = do(info)
        >>> ret['rc'] == RetCode.USERID_EXIST
        True
        >>> info['userid'] = '2';
        >>> info['name'] = 'tester2';
        >>> ret = do(info)
        >>> ret['rc'] == RetCode.OK
        True
        """
        
        ret = dict()
                   
        objby_userid = base.objects.filter(userid=info['userid'])
        objby_name = base.objects.filter(name=info['name'])
        
        if len(objby_userid) != 0:
            ret['rc'] = RetCode.USERID_EXIST;
        elif len(objby_name) != 0:
            ret['rc'] = RetCode.NAME_EXIST;
        else:
            ret['rc'] = RetCode.OK
            obj = base(userid=info['userid'],
                       pwd=info['pwd'],
                       name=info['name'],
                       regip=['ip'],
                       ip=['ip'],
                       status=base.STATUS_NORMAL,
                       date_lastlogin=timezone.now(),
                       date_create=timezone.now())
            obj.save()
        

        return ret