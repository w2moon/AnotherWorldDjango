
"""
basedata test 
>>> travellerbase[1]['id']
1
>>> soulbase[1]['id']
1
>>> equipmentbase[1]['id']
1
>>> buffbase[1000]['id']
1000
>>> skillbase[1000]['id']
1000
"""

import wl

MAX_BATTLE_TURN = 30
ACTION_INTERVAL = 0
HERO_IDX = 4

EQUIP_WEAPONR = 0
EQUIP_WEAPONL = 1
EQUIP_CLOTH = 2
EQUIP_TRINKET = 3
EQUIP_NUM = 4

WEAPON_MAINHAND = 0
WEAPON_OFFHAND = 1
WEAPON_ONEHAND = 2
WEAPON_TWOHAND = 3

TOTAL_POINT = 18

rolecfg = wl.csv_cfg("../AnotherWorldData/rolecfg.csv")


lotterypool = wl.csv_idmap("../AnotherWorldData/lotterypool.csv")
wl.csv_param(lotterypool,[ ["pool",[";",","]] ])

rolelevel = wl.csv_idmap("../AnotherWorldData/rolelevel.csv")

submaps = wl.csv_idmap("../AnotherWorldData/submaps.csv")
wl.csv_param(submaps,[ ["stages",[","]] ])

material = wl.csv_idmap("../AnotherWorldData/material.csv")
blueprint = wl.csv_idmap("../AnotherWorldData/blueprint.csv")

enemy = wl.csv_idmap("../AnotherWorldData/enemy.csv")
stage = wl.csv_idmap("../AnotherWorldData/stage.csv")
wl.csv_param(stage,[ ["rewardfirst",[";",","]],["reward",[";",","]],["enemy",[";",","]] ])

travellerbase = wl.csv_idmap("../AnotherWorldData/travellerbase.csv")

travellerskill = wl.csv_idmap("../AnotherWorldData/travellerskill.csv")
wl.csv_param(travellerskill,[ ["common",[","]],["uncommon",[","]] ])

soulbase = wl.csv_idmap("../AnotherWorldData/soulbase.csv")
equipmentbase = wl.csv_idmap("../AnotherWorldData/equipmentbase.csv")

buffbase = wl.csv_idmap("../AnotherWorldData/buffbase.csv")
wl.csv_param(buffbase,[ ["startlogic",[";",","]],["intervallogic",[";",","]],["endlogic",[";",","]] ])

skillbase = wl.csv_idmap("../AnotherWorldData/skillbase.csv")
wl.csv_param(skillbase,[ ["condition",[";",","]],["param",[","]] ])

rarityclass = wl.csv_idmap("../AnotherWorldData/rarityclass.csv")
wl.csv_param(rarityclass,[ ["starupcopper",[","]] ])

lang ={
       }

combineid = {}

combineidex = {}

combinerace = {}

combineraceex = {}

mutation = {}

for k,info in soulbase.items():
    if info['canmutate'] == 1:
        if not mutation.has_key(info['rarityclass']):
            mutation[info['rarityclass']] = []
        mutation[info['rarityclass']].append(k)
        
    if info['fatherid'] != 0:
        if not combineid.has_key(info['fatherid']):
            combineid[info['fatherid']] = {'mapid':{},'maptype':{}}
        if info['motherid'] != 0:
            combineid[info['fatherid']]['mapid'][info['motherid']] = info['id']
        else:
            combineid[info['fatherid']]['maptype'][info['motherrace']] = info['id']
            
        
    if info['fatherrace'] != 0:
        if not combinerace.has_key(info['fatherrace']):
            combinerace[info['fatherrace']] = {'mapid':{},'maptype':{}}
        if info['motherid'] != 0:
            combinerace[info['fatherrace']]['mapid'][info['motherid']] = info['id']
        else:
            combinerace[info['fatherrace']]['maptype'][info['motherrace']] = info['id']
            
    if info['motherid'] != 0:
        if not combineidex.has_key(info['motherid']):
            combineidex[info['motherid']] = {'mapid':{},'maptype':{}}
        if info['fatherid'] != 0:
            combineidex[info['motherid']]['mapid'][info['fatherid']] = info['id']
        else:
            combineidex[info['motherid']]['maptype'][info['fatherrace']] = info['id']
    
    if info['motherrace'] != 0:
        if not combineraceex.has_key(info['motherrace']):
            combineraceex[info['motherrace']] = {'mapid':{},'maptype':{}}
        if info['fatherid'] != 0:
            combineraceex[info['motherrace']]['mapid'][info['fatherid']] = info['id']
        else:
            combineraceex[info['motherrace']]['maptype'][info['fatherrace']] = info['id']
            
def get_combineid(soulbaseid1,soulbaseid2):
    soultype1 = soulbase[soulbaseid1]['race']
    soultype2 = soulbase[soulbaseid2]['race']
    if combineid.has_key(soulbaseid1):
        if combineid[soulbaseid1]['mapid'].has_key(soulbaseid2):
            return combineid[soulbaseid1]['mapid'][soulbaseid2]
        if combineid[soulbaseid1]['maptype'].has_key(soultype2):
            return combineid[soulbaseid1]['maptype'][soultype2]
        
    if combinerace.has_key(soultype1):
        if combinerace[soultype1]['mapid'].has_key(soulbaseid2):
            return combinerace[soultype1]['mapid'][soulbaseid2]
        if combinerace[soultype1]['maptype'].has_key(soultype2):
            return combinerace[soultype1]['maptype'][soultype2]
        
    if combineidex.has_key(soulbaseid2):
        if combineidex[soulbaseid2]['mapid'].has_key(soulbaseid1):
            return combineidex[soulbaseid2]['mapid'][soulbaseid1]
        if combineidex[soulbaseid2]['maptype'].has_key(soultype1):
            return combineidex[soulbaseid2]['maptype'][soultype1]
        
    if combineraceex.has_key(soultype2):
        if combineraceex[soultype2]['mapid'].has_key(soulbaseid1):
            return combineraceex[soultype2]['mapid'][soulbaseid1]
        if combineraceex[soultype2]['maptype'].has_key(soultype1):
            return combineraceex[soultype2]['maptype'][soultype1]
        
    return None

def get_levelup_exp(curlevel,rarity):
    return curlevel + curlevel*curlevel*rarity


def get_rolecfg():
    return rolecfg

def get_info(base,iid):
    if base.has_key(iid):
        return base[iid]
    return None

targettype = {
              'none':'none',
              'enemy':'enemy',
              'ally':'ally',
              'all':'all',
              'self':'self',
              'onlyallyfront':'onlyallyfront',
              'onlyallyhero':'onlyallyhero',
              'onlyenemyfront':'onlyenemyfront',
              'onlyenemyhero':'onlyenemyhero',
              'eventtrigger':'eventtrigger',
              'eventtarget':'eventtarget',
              'selected':'selected',
              }


