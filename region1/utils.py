"""
utils
>>> log_create("1")
>>> log_login("1")
>>> log_charge("1",1)
>>> log_shop("1",1,1)
>>> info = data.stage[1001]
>>> r = logic.role.role.create_from_enemy(info['enemy'],1,info['hero'])
"""
from django.utils import timezone

from account.models import base

from data.retcode import RetCode

import gamelog.models as log

import logic
import data

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

def req_friends(owner_userid,start,end):
    pass

def req_applicants(owner_userid,start,end):
    pass

def send_applicant(owner_userid,userid):
    pass

def delete_applicant(owner_userid,userid):
    pass

def apply_applicant(owner_userid,userid):
    pass

 

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

def battle_pve(info):
    r = get_role(info['userid'])
    
    if r.getHero() == None:
        return RetCode.BATTLE_NOTHAVEHERO
    
    stageinfo = data.stage[info['stage_id']]
    
    if r.level < stageinfo['levelneed']:
        return RetCode.BATTLE_LOW_LEVEL
    
    if r.hp < stageinfo['hpcost']:
        return RetCode.BATTLE_LOW_HP
    
    if not r.isCompleteStage(stageinfo['stageneed'],info['level']-1):
        return RetCode.BATTLE_NOT_COMPLETE_PRESTAGE
    
    has = False
    for stageid in data.submaps[info['submap']]['stages']:
        if stageid == info['stage_id']:
            has = True
    
    if not has:
        return RetCode.BATTLE_WRONG_MAP
    
    if stageinfo['hpcost'] != 0:
        r.hp = r.hp - stageinfo['hpcost']
        r.save()
        
    for e in stageinfo['enemy']:
        if e[0] != 0:
            r.meet(data.enemy[e[0]]['soulid'])
        
    for e in stageinfo['hero']:
        if e[0] != 0:
            r.meet(data.enemy[e[0]]['soulid'])
    
    bf = logic.battlefield.battlefield(stageinfo,r.packforother(),info['level'])
    
    while not bf.isFinished():
        bf.turn_process()
     
   
    if bf.result == True:
        #reward
        return RetCode.BATTLE_RESULT_WIN
    else:
        return RetCode.BATTLE_RESULT_FAIL
    