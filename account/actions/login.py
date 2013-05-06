'''
Created on Apr 21, 2013

@author: w2moon
'''
from django.utils import timezone
from django.core.cache import cache


import random

from retcode import RetCode
from account.models import base

def do(info):
        """
        login test
        >>> from account.actions.register import do as register
        >>> reginfo={'userid':'1','pwd':'123','name':'tester','ip':'127.0.0.1'}
        >>> ret = register(reginfo)
        >>> info={'userid':'1','pwd':'123','ver':'1','ip':'127.0.0.1','region':'region1'}
        >>> ret = do(info)
        >>> ret['rc'] == RetCode.OK
        True
        >>> info['pwd']='222'
        >>> ret = do(info)
        >>> ret['rc'] == RetCode.PWD_ERROR
        True
        """
        ret = dict()
        
        obj = base.objects.filter(userid=info['userid'])
        if len(obj) == 0 :
            ret['rc'] = RetCode.USERID_NOTEXIST
            return ret
        else:
            obj = obj[0]

        if obj.pwd != info['pwd']:
            ret['rc'] = RetCode.PWD_ERROR;
            return ret
        ret['rc'] = RetCode.OK;
        ret['region'] = info['region']
        ret['session'] = random.randint(0,1000000)
        cache.set('user'+obj.userid,ret['session'],60*10)
        obj.session = ret['session']
        obj.date_lastlogin = timezone.now()
        obj.region = info['region']
        obj.ip = info['ip']
        obj.save()
        ret['id'] = obj.id
        ret['name'] = obj.name

        return ret