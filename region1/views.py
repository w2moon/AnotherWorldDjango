
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import hashlib
import json
import glob
import os

from django.core.cache import cache

from account.models import base

from django.conf import settings
SECRET_KEY = settings.SECRET_KEY

actions = {}
path = os.path.dirname(__file__)
packname = os.path.basename(path)+".actions."

for action in glob.glob(path+"/actions/*.py"):
        name = os.path.splitext(os.path.basename(action))[0]
        if name != "__init__":
                exec("import "+packname+name)
                actions[name] = eval("reload("+packname+name+")").do
@csrf_exempt
def index(request,sig):
        """
        region view test
        >>> a = cache.set("hello",1111)
        >>> cache.get("hello") == 1111
        True
        """
        for k in request:
                t = k
                break

        if hasattr(request,'body'):
                info = request.body
        elif t is not None:
                info = t
        else:
                return HttpResponse('{"rc":1000}')

        if hashlib.md5(info+SECRET_KEY).hexdigest() != sig:
                return HttpResponse('{"rc":1000}')

        info = json.loads(info)
        
        session = cache.get('ol:'+info['userid'])
        if session != info['session']:
            obj = base.objects.filter(userid=info['userid'])
            if obj.count() == 0 or obj.session != info['session']:
                return HttpResponse('{"rc":2005}')
            
        cache.set('ol:'+info['userid'],info['session'],settings.CACHE_TIME)
        
        
        ret = actions[info['code']](info)

        ret = json.dumps(ret)
        return HttpResponse(ret)
