
import wl

from models import usermail
from models import sysmail
from models import developermail
from models import sysreaded
from django.utils import timezone
from django.db.models import Q
def get_object(model,param):
    objs = model.objects.filter(**param)
    if objs.count() == 0:
        return None
    else:
        return objs[0]

def user_send(title,content,attachment,sender_userid,sender_name,reciever_userid,date = None):
    if date == None:
        date = timezone.now()
    m = usermail(userid=reciever_userid,title=title,content=content,attachment=attachment,issys=0,sender_userid=sender_userid,sender_name=sender_name,date=date)
    m.save()
    return m

def developer_send(title,content,attachment,sender_userid,sender_name,date = None):
   
    if date == None:
        date = timezone.now()
    m = developermail(title=title,content=content,attachment=attachment,sender_userid=sender_userid,sender_name=sender_name,date=date)
    m.save()
    return m

def sys_send(title,content,attachment,reciever_userid,date = None):
    if date == None:
        date = timezone.now()
    m = usermail(userid=reciever_userid,title=title,content=content,attachment=attachment,issys=1,date=date)
    m.save()
    return m

def sys_add(title,content,attachment,date = None):
    if date == None:
        date = timezone.now()
    m = sysmail(title=title,content=content,attachment=attachment,date=date)
    m.save()
    return m

def recieve_sys(userid):
    objs = sysreaded.objects.filter(userid=userid).values('mailid')
    mails = sysmail.objects.exclude(id__in = objs)
    for m in mails:
        sys_send(m.title,m.content,m.attachment,userid,date=m.date)
        s = m.sysreaded_set.create(userid=userid)
        s.save()
        
    

def get_mail(mid):
    return get_object(usermail,{'id':mid})

def get_sys(mid):
    return get_object(sysmail,{'id':mid})

def get_mail_num(userid):
    return usermail.objects.filter(userid=userid).count()

def get_all_mail(userid):
    mails = []
    
    t = usermail.objects.filter(userid=userid)
    for v in t:
        mails.append(v.pack())
        
    return mails