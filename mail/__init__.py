
from models import usermail
from models import sysmail
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
    return sysmail.objects.raw("select * from mail_sysmail where id not in(select mailid from mail_sysreaded where userid='%s')",[userid])
    

def get_mail(mid):
    return get_object(usermail,{'id':mid})

def get_sys(mid):
    return get_object(sysmail,{'id':mid})

def get_all_mail(userid):
    mails = []
    
    t = usermail.objects.filter(userid=userid)
    for v in t:
        mails.append(v.pack())
        
    return mails