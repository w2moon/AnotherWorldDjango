from django.db import models


class create(models.Model):
        id = models.AutoField(primary_key=True)
        userid = models.CharField(max_length=32,db_index=True)
        ver = models.IntegerField(max_length=4,default=0)
        date = models.DateTimeField()

        def __unicode__(self):
                return "create log ver:%u userid:%s  date:%s" % (self.ver,self.userid,self.date)
            
class login(models.Model):
        id = models.AutoField(primary_key=True)
        userid = models.CharField(max_length=32,db_index=True)
        ver = models.IntegerField(max_length=4,default=0)
        date = models.DateTimeField()

        def __unicode__(self):
                return "login log ver:%u userid:%s id:%u date:%s" % (self.ver,self.userid,self.id,self.date)

class charge(models.Model):
        id = models.AutoField(primary_key=True)
        userid = models.CharField(max_length=32,db_index=True)
        ver = models.IntegerField(max_length=4,default=0)
        date = models.DateTimeField()
        value = models.IntegerField(max_length=4,default=0)

        def __unicode__(self):
                return "charge log ver:%u userid:%s id:%u date:%s value:%u" % (self.ver,self.userid,self.id,self.date,self.value)
            
class shop(models.Model):
        id = models.AutoField(primary_key=True)
        userid = models.CharField(max_length=32,db_index=True)
        ver = models.IntegerField(max_length=4,default=0)
        date = models.DateTimeField()
        type = models.IntegerField(max_length=4,default=0)
        value = models.IntegerField(max_length=4,default=0)

        def __unicode__(self):
                return "charge log ver:%u userid:%s id:%u date:%s type:%u value:%u" % (self.ver,self.userid,self.id,self.date,self.type,self.value)