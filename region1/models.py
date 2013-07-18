from django.db import models
from django.utils import timezone

import time
import re

import wl

isdate = re.compile(r'^date')

class role(models.Model):
    userid = models.CharField(max_length=32,primary_key=True)
    name = models.CharField(max_length=32)
    id = models.IntegerField(max_length=4,unique=True)
    exp = models.IntegerField(max_length=4,default=0)
    level = models.IntegerField(max_length=4,default=1)
    hp = models.IntegerField(max_length=4,default=0)
    copper = models.IntegerField(max_length=4,default = 0)
    gold = models.IntegerField(max_length=4,default = 0)
    
    charged = models.IntegerField(max_length=4,default = 0)
    checkin_num = models.IntegerField(max_length=4,default = 0)
    
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
    
    
    def get_object(self,sets,param):
        objs = sets.filter(**param)
        if objs.count() == 0:
            return None
        else:
            return objs[0]
    
    def get_traveller(self,tid):
        return self.get_object(self.traveller_set,{'id':id}) 
    
    def create_traveller(self):
        return self.traveller_set.create()
    
    def get_soul(self,tid):
        return self.get_object(self.soul_set,{'id':id}) 
    
    def create_soul(self,baseid):
        soul = self.soul_set.create(baseid=baseid)
        #is this save really need?
        soul.save()
        return soul
    
    def get_equipment(self,tid):
        return self.get_object(self.equipment_set,{'id':id}) 
    
    def create_equipment(self,baseid):
        equipment = self.equipment_set.create(baseid=baseid)
        #is this save really need?
        equipment.save()
        return equipment
    
    def new_randstate(self):
        randstate = self.get_randstate()
        if randstate == None:
            state = self.rand_state_set.create()
        state.seed(self.userid+str(timezone.now()))
       
        state.save()
        
    def get_randstate(self):
        objs = self.rand_state_set.all()
        if objs.count() != 0:
            return objs[0]
        return None
    
    def rand(self):
        self.get_randstate().rand()
        
    def save_rand(self):
        self.get_randstate().save()
        
    
    def packforself(self):
        player = {}
        for k in self._meta.fields:
            if isdate.match(k.name):
                player[k.name] = time.mktime(getattr(self,k.name).timetuple())
            else: 
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
    
    
class rand_state(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(role)
    state = models.TextField(default="")
    
    rand_inst = None
    
    def get_inst(self):
        if self.rand_inst == None:
            self.rand_inst = wl.rand.rand()
            self.rand_inst.unpack_str(self.state)
        return self.rand_inst
    
    def save(self, *args, **kwargs):
        self.state = self.get_inst().pack_str()
        super(rand_state, self).save(*args, **kwargs) 
        
    """
    need save first
    """
    def reset(self):
        self.get_inst().unpack_str(self.state)
    
    def seed(self,s):
        return self.get_inst().seed(s)
    
    def rand(self):
        return self.get_inst().random()
    
    def __unicode__(self):
        return "rand state"
    
class equipment(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(role)
    baseid = models.IntegerField(max_length=4,default=0)
    
    travellerid = models.IntegerField(max_length=4,default=0)
    
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
    
    travellerid = models.IntegerField(max_length=4,default=0)
    
    star = models.IntegerField(max_length=4,default=1)
    
    exp = models.IntegerField(max_length=4,default=0)
    level = models.IntegerField(max_length=4,default=1)
    
    skillexp = models.IntegerField(max_length=4,default=0)
    skilllevel = models.IntegerField(max_length=4,default=0)
    
    
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
    gender = models.IntegerField(max_length=1,default=0)
    age = models.IntegerField(max_length=1,default=0)
    exp = models.IntegerField(max_length=4,default=0)
    level = models.IntegerField(max_length=4,default=1)
    
    MaxHP = models.IntegerField(max_length=4,default=0)
    Attack = models.IntegerField(max_length=4,default=0)
    Defense = models.IntegerField(max_length=4,default=0)
    Heal = models.IntegerField(max_length=4,default=0)
        
    skill1id = models.IntegerField(max_length=4,default=0)
    skill1exp = models.IntegerField(max_length=4,default=0)
    skill1level = models.IntegerField(max_length=4,default=0)
    
    skill2id = models.IntegerField(max_length=4,default=0)
    skill2exp = models.IntegerField(max_length=4,default=0)
    skill2level = models.IntegerField(max_length=4,default=0)
    
    nature = models.IntegerField(max_length=4,default=0)
       
    soulid = models.IntegerField(max_length=4,default=0)
    
    weaponid = models.IntegerField(max_length=4,default=0)
    clothid = models.IntegerField(max_length=4,default=0)
    trinketid = models.IntegerField(max_length=4,default=0)
    
    img = models.TextField(default="")
    
    MALE = 0
    FEMAIL = 1
    
    CHILD = 0
    YOUNG = 1
    ADULT = 2
    ELDER = 3
    def pack(self):
        t = {}
        for k in self._meta.fields:
            if k.name != 'owner': 
                t[k.name] = getattr(self,k.name)
                        
        return t
    
    def __unicode__(self):
        return "traveller %s" % (self.name)
    
