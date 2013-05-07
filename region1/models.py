from django.db import models

from django.core import serializers

class role(models.Model):
    userid = models.CharField(max_length=32,primary_key=True)
    name = models.CharField(max_length=32,unique=True)
    id = models.IntegerField(max_length=4,unique=True)
    exp = models.IntegerField(max_length=4,default=0)
    level = models.IntegerField(max_length=4,default=1)
    hp = models.IntegerField(max_length=4,default=0)
    copper = models.IntegerField(max_length=4,default = 0)
    gold = models.IntegerField(max_length=4,default = 0)
    
    charged = models.IntegerField(max_length=4,default = 0)
    
    lastseed = models.IntegerField(max_length=4,default = 0)
    
    slot1 = models.IntegerField(max_length=4,default = 0)
    slot2 = models.IntegerField(max_length=4,default = 0)
    slot3 = models.IntegerField(max_length=4,default = 0)
    slot4 = models.IntegerField(max_length=4,default = 0)
    slot5 = models.IntegerField(max_length=4,default = 0)
    
    extrasoulnum = models.IntegerField(max_length=4,default = 0)
    extraequipmentnum = models.IntegerField(max_length=4,default = 0)
    extratravellernum = models.IntegerField(max_length=4,default = 0)
    
    date_lastupdate = models.DateTimeField()
    date_lastenter = models.DateTimeField()
    date_create = models.DateTimeField()
    
    def packforself(self):
        player = {}
        for k in self._meta.fields:
            player[k.name] = getattr(self,k.name)
            
        player['equipments'] = []
        for equip in self.equipment_set.all():
            player['equipments'].append(equip.pack())
            
        player['souls'] = []
        for soul in self.soul_set.all():
            player['souls'].append(soul.pack())
        
        player['travellers'] = []
        for traveller in self.traveller_set.all():
            player['travellers'].append(traveller.pack())
        
        return player
      
    def __unicode__(self):
        return "role userid:%s name:%s" % (self.userid,self.name)
    
    
class equipment(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(role)
    baseid = models.IntegerField(max_length=4,default=0)
    
    exp = models.IntegerField(max_length=4,default=0)
    level = models.IntegerField(max_length=4,default=1)
    
    def pack(self):
        t = {}
        for k in self._meta.fields:
            if k.name != 'owner': 
                t[k.name] = getattr(self,k.name)
        return t
    
    def __unicode__(self):
        return "equipment %d" % (self.baseid)
    
class soul(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(role)
    baseid = models.IntegerField(max_length=4,default=0)
    
    exp = models.IntegerField(max_length=4,default=0)
    level = models.IntegerField(max_length=4,default=1)
    
    def pack(self):
        t = {}
        for k in self._meta.fields:
            if k.name != 'owner': 
                t[k.name] = getattr(self,k.name)
        return t
    
    def __unicode__(self):
        return "soul %d" % (self.baseid)
    
class traveller(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(role)
    
    name = models.CharField(max_length=32)
    exp = models.IntegerField(max_length=4,default=0)
    level = models.IntegerField(max_length=4,default=1)
    
    view = models.IntegerField(max_length=1,default=2) #VIEW_SELF
    
    skillid = models.IntegerField(max_length=4,default=0)
    talentid = models.IntegerField(max_length=4,default=0)
    
    
    soulid = models.IntegerField(max_length=4,default=0)
    weaponid = models.IntegerField(max_length=4,default=0)
    clothid = models.IntegerField(max_length=4,default=0)
    trinketid = models.IntegerField(max_length=4,default=0)
    
    img = models.TextField(default="")
    
    VIEW_SELF = 0
    VIEW_FRIEND = 1
    VIEW_ALL = 2
    
    def pack(self):
        t = {}
        for k in self._meta.fields:
            if k.name != 'owner': 
                t[k.name] = getattr(self,k.name)
        return t
    
    def __unicode__(self):
        return "traveller %s" % (self.name)