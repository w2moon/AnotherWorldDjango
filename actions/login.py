'''
Created on Apr 21, 2013

@author: w2moon
'''
from django.utils import timezone
from django.core.cache import cache

import random

from account.models import base

def do(info):
        """
        login test
        >>> info={'userid':'1','pwd':'123','ip':'127.0.0.1'}
        >>> ret = do(info)
        >>> ret['result']
        True
        >>> info['pwd']='222'
        >>> ret = do(info)
        >>> ret['result']
        False
        """
        obj = base.objects.filter(userid=info['userid'])
        if len(obj) == 0 :
                obj = base(userid=info['userid'],pwd=info['pwd'],date_create=timezone.now())
        else:
            obj = obj[0]

        ret = dict()
        if obj.pwd == info['pwd']:
                ret['result'] = True
                ret['region'] = obj.region
        else:
                ret['result'] = False

        ret['session'] = random.randint(0,1000000)
        cache.set('user'+obj.userid,ret['session'],60*10)
        obj.session = ret['session']
        obj.date_lastlogin = timezone.now()
        obj.ip = info['ip']
        obj.save()
        ret['id'] = obj.id

        return ret