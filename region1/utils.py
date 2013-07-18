"""
utils
>>> log_create("1")
>>> log_login("1")
>>> log_charge("1",1)
>>> log_shop("1",1,1)
"""
from django.utils import timezone

from account.models import base

import gamelog.models as log


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

def log_create(userid):
    l = log.create(userid=userid,date=timezone.now(),ver=0)
    l.save()
    
def log_login(userid):
    l = log.login(userid=userid,date=timezone.now(),ver=0)
    l.save()
    
def log_charge(userid,value):
    l = log.charge(userid=userid,date=timezone.now(),value=value,ver=0)
    l.save()
    
def log_shop(userid,itemtype,value):
    l = log.shop(userid=userid,date=timezone.now(),type=itemtype,value=value,ver=0)
    l.save()