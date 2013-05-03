from django.db import models

class region(models.Model):
    name = models.CharField(max_length=32,primary_key=True)
    url = models.CharField(max_length=256)
    
    def __unicode__(self):
        return "region"

class base(models.Model):
        id = models.AutoField(primary_key=True)
        userid = models.CharField(max_length=32,unique=True)
        pwd = models.CharField(max_length=32)
        region_name = models.CharField(max_length=16)
        ip = models.CharField(max_length=16)
        session = models.CharField(max_length=16)
        date_create = models.DateTimeField()
        date_lastlogin = models.DateTimeField()

        def __unicode__(self):
                return "userid:%s id:%u region:%s ip=%s date_create:%s date_lastlogin:%s" % (self.userid,self.id,self.region,self.ip,self.date_create,self.date_lastlogin)
