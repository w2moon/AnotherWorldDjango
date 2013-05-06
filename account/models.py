from django.db import models

class region(models.Model):
    name = models.CharField(max_length=32,primary_key=True)
    url = models.CharField(max_length=256)
    status = models.IntegerField(max_length=1) #0 normal,1 full,2 maintain
    recommend = models.IntegerField(max_length=1) #0 normal,1 recommend
    
    STATUS_NORMAL = 0
    STATUS_FULL = 1
    STATUS_MAINTAIN = 2
    
    def __unicode__(self):
        return "region:%s url:%s status:%d recommend:%d" % (self.name,self.url,self.status,self.recommend)

class base(models.Model):
        id = models.AutoField(primary_key=True)
        userid = models.CharField(max_length=32,unique=True)
        pwd = models.CharField(max_length=32)
        name = models.CharField(max_length=32,unique=True) 
        status = models.IntegerField(max_length=1) #0normal 1banned
        region = models.CharField(max_length=16)
        ip = models.CharField(max_length=16)
        regip = models.CharField(max_length=16)
        session = models.CharField(max_length=16)
        date_create = models.DateTimeField()
        date_lastlogin = models.DateTimeField()
        
        
        STATUS_NORMAL = 0
        STATUS_BANNED = 1

        def __unicode__(self):
                return "userid:%s id:%u region:%s ip=%s date_create:%s date_lastlogin:%s" % (self.userid,self.id,self.region,self.ip,self.date_create,self.date_lastlogin)
