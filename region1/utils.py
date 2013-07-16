'''
Created on 2013-7-16

@author: pengw
'''
from django.utils import timezone

from account.models import base

arr = __file__.split('/')
appname = arr[len(arr)-2]

exec("import "+appname)
role = eval("reload("+appname+".models)").role

def get_object(model,param):
    objs = model.objects.filter(**param)
    if objs.count() == 0:
        return None
    else:
        return objs[0]

def get_account(userid):
    return get_object(base,{'userid':userid})

def create_role(rid,userid,name):
    time = timezone.now()
    return role(id=rid,userid=userid,name=name,date_lastupdate=time,date_lastenter=time,date_create=time)
    
def get_role(userid):
    return get_object(role,{'userid':userid})

    