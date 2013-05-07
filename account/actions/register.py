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
        >>> info={'userid':'2','pwd':'123','ip':'127.0.0.1'}
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
        
        if len(objby_userid) != 0:
            ret['rc'] = RetCode.USERID_EXIST;
        else:
            ret['rc'] = RetCode.OK
            obj = base(userid=info['userid'],
                       pwd=info['pwd'],
                       regip=info['ip'],
                       ip=info['ip'],
                       status=base.STATUS_NORMAL,
                       date_lastlogin=timezone.now(),
                       date_create=timezone.now())
            obj.save()
            
        ret['userid'] = info['userid']
        ret['pwd'] = info['pwd']        
        

        return ret