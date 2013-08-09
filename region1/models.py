from django.db import models
from django.utils import timezone

import time
import re
import data
import wl
import random as sysrand

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
    
    SLOT_NUM = 5
    
    COMPLETE_FIRST = 0
    COMPLETE_LEVEL = 2
    COMPLETE_OK = 1
    
    def getUserid(self):
        return self.userid
    
    def getStage(self,stageid):
        return self.get_object(self.stage_set,{'stage_id':stageid})
    
    def isCompleteStage(self,stageid,level):
        if stageid == 0:
            return True
        stage = self.getStage(stageid)
        return stage != None and (level == 1 or level <= stage.level)
    
    def completeStage(self,stageid,level):
        stage = self.getStage(stageid)
        if stage == None:
            stage = self.stage_set.create(stage_id=stageid)
            stage.level = level
            stage.save()
            return role.COMPLETE_FIRST
        
        if level > stage.level :
            stage.level = level
            stage.save()
            return role.COMPLETE_LEVEL
            
        return role.COMPLETE_OK
    
    def getMaxSoulNum(self):
        return self.extrasoulnum + data.rolelevel[self.level]['maxsoulnum']
    
    def getMaxEquipNum(self):
        return self.extrasoulnum + data.rolelevel[self.level]['maxequipnum']
    
    def getMaxTravellerNum(self):
        return self.extrasoulnum + data.rolelevel[self.level]['maxtravellernum']
    
    def addReward(self,reward,level = 1):
        
        equipments =[]
        souls = []
        addexp = 0
        addhp = 0
        addcopper = 0
        addgold = 0
        addlevel = 0
        addextrasoulnum = 0
        addextraequipmentnum = 0
        addextratravellernum = 0
        for r in reward:
            if self.rand() < r[0]:
                if r[1] == 'addCopper' or r[1] == 'addExp':
                    o = getattr(self,r[1])(r[2]*level)
                else:
                    o = getattr(self,r[1])(*(r[2:]))
                if o != None:
                    if r[1] == "addEquip":
                        equipments.append(o.pack())
                    elif r[1] == "addSoul":
                        souls.append(o.pack())
                    elif r[1] == "lotteryPool":
                        equipments = equipments + o['equipments']
                        souls = souls + o['souls']
                        addexp += o['addexp']
                        addhp += o['addhp']
                        addcopper += o['addcopper']
                        addgold += o['addgold']
                        addlevel += o['addlevel']
                        addextrasoulnum += o['addextrasoulnum']
                        addextraequipmentnum += o['addextraequipmentnum']
                        addextratravellernum += o['addextratravellernum']
                    elif r[1] == "addExp":
                        addexp += r[2]
                    elif r[1] == "addHP":
                        addhp += r[2]
                    elif r[1] == "addCopper":
                        addcopper += r[2]
                    elif r[1] == "addGold":
                        addgold += r[2]
                    elif r[1] == "addLevel":
                        addlevel += r[2]
                    elif r[1] == "addExtraSoulNum":
                        addextrasoulnum += r[2]
                    elif r[1] == "addExtraEquipmentNum":
                        addextraequipmentnum += r[2]
                    elif r[1] == "addExtraTravellerNum":
                        addextratravellernum += r[2]
                        
                        
                        
        return {
               'hp':self.hp,
               'copper' : self.copper,
               'gold' : self.gold,
               'exp' : self.exp,
               'level' : self.level,
               'extrasoulnum' : self.extrasoulnum,
               'extraequipmentnum' : self.extraequipmentnum,
               'extratravellernum' : self.extratravellernum,
               
               'addexp' : addexp,
               'addhp' : addhp,
               'addcopper' :addcopper,
               'addgold' :addgold,
               'addlevel' :addlevel,
               'addextrasoulnum' :addextrasoulnum,
               'addextraequipmentnum' :addextraequipmentnum,
               'addextratravellernum' :addextratravellernum,
               
               'equipments' : equipments,
               'souls' : souls,
               }
        
    def lotteryPool(self,pid):
        return self.addReward(data.lotterypool[pid]['pool'],1)
        
    def addExtraSoulNum(self,v):
        self.extrasoulnum += v
        
    def addExtraEquipmentNum(self,v):
        self.extraequipmentnum += v
        
    def addExtraTravellerNum(self,v):
        self.extratravellernum += v
        
    def addCopper(self,v):
        self.copper += v
        
    def addGold(self,v):
        self.gold += v
        
    def addHP(self,v):
        self.hp = wl.clamp(self.hp+v, 0, data.rolelevel[self.level]['maxhp'])
        
    def onLevelup(self):
        self.hp = data.rolelevel[self.level]['maxhp']
        
    def addExp(self,v):
        if data.rolelevel.has_key(self.level + 1):
            self.exp += v
            if self.exp >= data.rolelevel[self.level]['exp']:
                self.level += 1
                self.exp -= data.rolelevel[self.level]['exp']
                
                self.onLevelup()
        else:
            self.exp = 0
            
        for i in xrange(1,self.SLOT_NUM+1):
            traveller = self.getTraveller(getattr(self,"slot"+str(i)))
            if traveller == None:
                continue
            traveller.addExp(v)
            soul = self.getSoul(traveller.soulid)
            if soul == None:
                continue
            soul.addExp(v)
            
        
    def addLevel(self,v):
        self.level = wl.clamp(self.level+v, 0, len(data.rolelevel))
        
        self.onLevelup()
    
    def get_object(self,sets,param):
        objs = sets.filter(**param)
        if objs.count() == 0:
            return None
        else:
            return objs[0]
        
    def getHero(self):
        if self.slot1 == 0:
            return None
        else:
            return self.getTraveller(self.slot1)
        
    def equipTraveller(self,slot,travellerid):
        setattr(self,slot,travellerid)
        self.save()
        
    def addSoul(self,soulid):
        soulbase = data.get_info(data.soulbase,soulid)
        if soulbase != None:
            soul = self.soul_set.create(baseid=soulid)
            soul.save()
            return soul
        return None
    
    def addEquip(self,equipid):
        equipbase = data.get_info(data.soulbase,equipid)
        if equipbase != None:
            equip = self.equipment_set.create(baseid=equipid)
            equip.save()
            return equip
        return None
    
    def findBlueprint(self,blueprintid):
        return self.get_object(self.blueprint_set,{'baseid':blueprintid})
    
    def addBlueprint(self,blueprintid):
        blueinfo = data.get_info(data.blueprint,blueprintid)
        if blueinfo != None:
            blueprint = self.findBlueprint(blueprintid)
            if blueprint != None:
                return blueprint
            blueprint = self.blueprint_set.create(baseid=blueprintid)
            blueprint.save()
            return blueprint
        return None
    
    def composeBlueprint(self,blueprintid):
        blueprint = self.findBlueprint(blueprintid)
        if blueprint == None:
            return None
        
        info = data.get_info(data.blueprint,blueprint.baseid)
        
        if self.copper < info['copper']:
            return None
        
        for i in xrange(1,7):
            if wl.tonumber(info["mid"+str(i)]) == 0:
                continue
            
            material = self.findMaterial(wl.tonumber(info["mid"+str(i)]))
            if material.num < wl.tonumber(info["mnum"+str(i)]):
                return None
            
        self.copper -= info['copper']
        self.save()
        
        for i in xrange(1,7):
            if wl.tonumber(info["mid"+str(i)]) == 0:
                continue
            
            material = self.findMaterial(wl.tonumber(info["mid"+str(i)]))
            material.num -= wl.tonumber(info["mnum"+str(i)])
            material.save()
            
        
        return self.addEquip(info['equipid'])
            
            
    
    def findMaterial(self,materialid):
        return self.get_object(self.material_set,{'baseid':materialid})
    
    def addMaterial(self,materialid,num):
        info = data.get_info(data.material,materialid)
        if info != None:
            material = self.findMaterial(materialid)
            if material == None:
                material = self.material_set.create(baseid=materialid)
            
            material.num += num
            material.save()
            return material
        return None
        
    def getRandList(self,tmin,tmax):
        arr = []
        for i in xrange(tmin,tmax+1):
            arr.append(i)
        ret = [-1]*len(arr)
        
        while len(arr) > 0:
            idx = self.rand()*len(arr)
            if ret[idx] != -1:
                continue
            ret[idx] = arr.pop()
        
        return ret
    
    def addTraveller(self,info,travellerbase):
        if self.traveller_set.count() >= self.getMaxTravellerNum():
            return None
        
        traveller = self.traveller_set.create()
        traveller.name = info['name']
        traveller.gender = info['gender']
        traveller.age = info['age']
        traveller.img = info['img']
        
        """
        traveller.MaxHP = travellerbase['MaxHP']
        traveller.Attack = travellerbase['Attack']
        traveller.Defense = travellerbase['Defense']
        traveller.Heal = travellerbase['Heal']
        
        traveller.skill1id = travellerbase['skill1id']
        traveller.skill2id = travellerbase['skill2id']
        """
        
        
        
        idx = int(self.rand()*4)
        
        if idx == 0:
            traveller.MaxHP = 10+self.rand()*2
        else:
            traveller.MaxHP = 15
            
        if idx == 1:
            traveller.Attack = 1+self.rand()*2
        else:
            traveller.Attack = 4
            
        if idx == 2:
            traveller.Defense = 1+self.rand()*2
        else:
            traveller.Defense = 4
        
        if idx == 3:
            traveller.Heal = 1+self.rand()*2
        else:
            traveller.Heal = 4
        
        if info['ishuman'] == 1:
            skills = None
            if self.rand()<0.8:
                skills = data.travellerskill[idx]['common']
            else:
                skills = data.travellerskill[idx]['uncommon']
            traveller.skill1id = skills[int(self.rand()*len(skills))]
        
        
        soul = self.addSoul(travellerbase['soulbaseid'])
        if soul != None:
            traveller.equip_soul(soul)
        
        weaponr = self.addEquip(travellerbase['weaponrbaseid'])
        if weaponr != None:
            traveller.equip_weaponr(weaponr)
            
        weaponl = self.addEquip(travellerbase['weaponlbaseid'])
        if weaponl != None:
            traveller.equip_weaponr(weaponl)
        
        cloth = self.addEquip(travellerbase['clothbaseid'])
        if cloth != None:
            traveller.equip_cloth(cloth)
        
        trinket = self.addEquip(travellerbase['trinketbaseid'])
        if trinket != None:
            traveller.equip_trinket(trinket)
        
            
        traveller.save()
        
        return traveller
            
    def getTraveller(self,tid):
        return self.get_object(self.traveller_set,{'id':tid}) 
    
    
    def getSlotTravellers(self):
        slots = []
        travellerid = 0
        for i in xrange(1,self.SLOT_NUM):
            travellerid = getattr(self,"slot"+str(i))
            if travellerid != 0:
                slots.append(self.getTraveller(travellerid))
            else:
                slots.append(None)
        return slots
    
    def getSoul(self,tid):
        return self.get_object(self.soul_set,{'id':tid}) 
    
   
    
    def getEquipment(self,tid):
        return self.get_object(self.equipment_set,{'id':tid}) 
    
    def findEquip(self,bid):
        return self.get_object(self.equipment_set,{'baseid':bid}) 
    
    def create_equipment(self,baseid):
        equipment = self.equipment_set.create(baseid=baseid)
        #is this save really need?
        equipment.save()
        return equipment
    
    def new_randstate(self):
        randstate = self.get_randstate()
        if randstate == None:
            randstate = self.rand_state_set.create()
        randstate.seed(self.userid+str(timezone.now()))
       
        randstate.save()
        
    def get_randstate(self):
        objs = self.rand_state_set.all()
        if objs.count() != 0:
            return objs[0]
        
        state = self.rand_state_set.create()
        state.seed(self.userid+str(timezone.now()))
        state.save()
        return state
    
    def rand(self):
        return self.get_randstate().rand()
        
    def save_rand(self):
        self.get_randstate().save()
    
    def packforother(self):
        player = {}
        player['name'] = self.name
        player['id'] = self.id
        
        player['equipments'] = []
        player['souls'] = []
        player['travellers'] = []
        
        for i in xrange(1,self.SLOT_NUM+1):
            slotid = 'slot'+str(i)
            player[slotid] = getattr(self,slotid)
            if player[slotid] != 0:
                traveller = self.getTraveller(player[slotid])
                if traveller != None:
                    player['travellers'].append(traveller.pack())
                
                    
                    if traveller.soulid != 0:
                        soul = self.getSoul(traveller.soulid)
                        player['souls'].append(soul.pack())
                        
                    
                    if traveller.weaponrid != 0:
                        weaponr = self.getEquipment(traveller.weaponrid)
                        player['equipments'].append(weaponr.pack())
                        
                    if traveller.weaponlid != 0:
                        weaponl = self.getEquipment(traveller.weaponlid)
                        player['equipments'].append(weaponl.pack())
                        
                    
                    if traveller.clothid != 0:
                        cloth = self.getEquipment(traveller.clothid)
                        player['equipments'].append(cloth.pack())
                        
                    
                    if traveller.trinketid != 0:
                        trinket = self.getEquipment(traveller.trinketid)
                        player['equipments'].append(trinket.pack())
        
        return player
    
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
    
    skillexp = models.IntegerField(max_length=4,default=0)
    skilllevel = models.IntegerField(max_length=4,default=0)
    
    def addExp(self,exp):
        self.exp += exp
        rarity = data.equipmentbase[self.baseid]['rarityclass']
        maxlevel = data.rarityclass[rarity]['maxlevel']
        needexp = data.get_levelup_exp(self.level,rarity)
        while self.exp >= needexp and self.level < maxlevel:
            self.level += 1
            self.exp -= needexp
            needexp = data.get_levelup_exp(self.level,rarity)
            
        if self.level >= maxlevel:
            self.exp = 0
    
    
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
    
    star = models.IntegerField(max_length=4,default=0)
    
    exp = models.IntegerField(max_length=4,default=0)
    level = models.IntegerField(max_length=4,default=1)
    
    skillexp = models.IntegerField(max_length=4,default=0)
    skilllevel = models.IntegerField(max_length=4,default=0)
    
    def addExp(self,exp):
        self.exp += exp
        rarity = data.equipmentbase[self.baseid]['rarityclass']
        maxlevel = data.rarityclass[rarity]['maxlevel']
        needexp = data.get_levelup_exp(self.level,rarity)
        while self.exp >= needexp and self.level < maxlevel:
            self.level += 1
            self.exp -= needexp
            needexp = data.get_levelup_exp(self.level,rarity)
            
        if self.level >= maxlevel:
            self.exp = 0
    
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
    
    weaponrid = models.IntegerField(max_length=4,default=0)
    weaponlid = models.IntegerField(max_length=4,default=0)
    clothid = models.IntegerField(max_length=4,default=0)
    trinketid = models.IntegerField(max_length=4,default=0)
    
    img = models.TextField(default="")
    
    MALE = 0
    FEMAIL = 1
    
    CHILD = 0
    YOUNG = 1
    ADULT = 2
    ELDER = 3
    
    def addExp(self,exp):
        if data.rolelevel.has_key(self.level + 1):
            self.exp += exp
            if self.exp >= data.rolelevel[self.level]['exp']:
                self.level += 1
                self.exp -= data.rolelevel[self.level]['exp']
        else:
            self.exp = 0
    
    def pack(self):
        t = {}
        for k in self._meta.fields:
            if k.name != 'owner': 
                t[k.name] = getattr(self,k.name)
                
        t['slot'] = [self.weaponrid,self.weaponlid,self.clothid,self.trinketid]
                        
        return t
    
    def takeoff_soul(self):
        if self.soulid != 0:
            soul = self.owner.getSoul(self.soulid)
            soul.travellerid = 0
            self.soulid = 0
            
            soul.save()
            self.save()
    
    def equip_soul(self,soul):
        self.takeoff_soul()
        
        self.soulid = soul.id
        soul.travellerid = self.id
        
        soul.save()
        self.save()
        
    def takeoff_weaponr(self):
        if self.weaponrid != 0:
            weaponr = self.owner.getEquipment(self.weaponrid)
            weaponr.travellerid = 0
            self.weaponrid = 0
            
            weaponr.save()
            self.save()
            
    def takeoff_weaponl(self):
        if self.weaponlid != 0:
            weaponl = self.owner.getEquipment(self.weaponlid)
            weaponl.travellerid = 0
            self.weaponlid = 0
            
            weaponl.save()
            self.save()
            
    def takeoff_cloth(self):
        if self.clothid != 0:
            cloth = self.owner.getEquipment(self.clothid)
            cloth.travellerid = 0
            self.clothid = 0
            
            cloth.save()
            self.save()
            
    def takeoff_trinket(self):
        if self.trinketid != 0:
            trinket = self.owner.getEquipment(self.trinketid)
            trinket.travellerid = 0
            self.trinketid = 0
            
            trinket.save()
            self.save()
        
    def equip_weaponr(self,weaponr):
        self.takeoff_weaponr()
        
        self.weaponrid = weaponr.id
        weaponr.travellerid = self.id
        
        weaponr.save()
        self.save()
        
    def equip_weaponl(self,weaponl):
        self.takeoff_weaponl()
        
        self.weaponlid = weaponl.id
        weaponl.travellerid = self.id
        
        weaponl.save()
        self.save()
        
    def equip_cloth(self,cloth):
        self.takeoff_cloth()
        
        self.clothid = cloth.id
        cloth.travellerid = self.id
        
        cloth.save()
        self.save()
        
    def equip_trinket(self,trinket):
        self.takeoff_trinket()
        
        self.trinketid = trinket.id
        trinket.travellerid = self.id
        
        trinket.save()
        self.save()
    
    def __unicode__(self):
        return "traveller %s" % (self.name)
    
class stage(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(role)
    
    stage_id = models.IntegerField(max_length=4,default=0)
    level = models.IntegerField(max_length=4,default=1)
    
    def __unicode__(self):
        return "stage %d" % (self.stage_id)
    
class material(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(role)
    
    baseid = models.IntegerField(max_length=4,default=0)
    num = models.IntegerField(max_length=4,default=0)
    
    def __unicode__(self):
        return "material %d" % (self.baseid)
    
class blueprint(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(role)
    
    baseid = models.IntegerField(max_length=4,default=0)
    
    def __unicode__(self):
        return "blueprint %d" % (self.baseid)
