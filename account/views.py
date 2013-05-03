
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import hashlib
import json
import glob
import os


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
        for k in request:
                t = k
                break

        if hasattr(request,'body'):
                info = request.body
        elif t is not None:
                info = t
        else:
                return HttpResponse('{"result":false}')

        if hashlib.md5(info+SECRET_KEY).hexdigest() != sig:
                return HttpResponse('{"result":false}')

        info = json.loads(info)
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                info['ip'] =  request.META['HTTP_X_FORWARDED_FOR']
        else:
                info['ip'] = request.META['REMOTE_ADDR']
        ret = actions[info['code']](info)

        ret = json.dumps(ret)
        return HttpResponse(ret)
