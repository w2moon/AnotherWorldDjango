from django.db import models

MAIL_UNREAD = 0
MAIL_READED = 1

def get_object(model,param):
    objs = model.objects.filter(**param)
    if objs.count() == 0:
        return None
    else:
        return objs[0]
    
import re
import time
isdate = re.compile(r'^date')
# Create your models here.
class usermail(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=32,db_index=True)
    status = models.IntegerField(max_length=1,default=MAIL_UNREAD)
    issys = models.IntegerField(max_length=1,default=0)
    
    date = models.DateTimeField()
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=1048)
    attachment = models.CharField(max_length=256)
    
    
    sender_userid = models.CharField(max_length=32)
    sender_name = models.CharField(max_length=32)
    
    def isReaded(self):
        return self.status == MAIL_READED
    
    def read(self):
        if self.status == MAIL_UNREAD:
            self.status = MAIL_READED
            self.save()
            
    def pack(self):
        ret = {}
        for k in self._meta.fields:
            if isdate.match(k.name):
                ret[k.name] = time.mktime(getattr(self,k.name).timetuple())
            else: 
                ret[k.name] = getattr(self,k.name)
        return ret
    
    class Meta:
        ordering = ['-date']
        
    def __unicode__(self):
            return "usermail"

class sysmail(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=1048)
    attachment = models.CharField(max_length=256)
    
    def isReaded(self,userid):
        return get_object(self.sysreaded_set,{'userid':userid}) != None
    
    def read(self,userid):
        readed = self.sysreaded_set.create(userid=userid)
        readed.save()
    
    class Meta:
        ordering = ['-date']
    
    def __unicode__(self):
            return "sysmail"
        
class sysreaded(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=32,db_index=True)
    mailid = models.ForeignKey(sysmail)
    
    def __unicode__(self):
            return "sysreaded"