
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

COPPER_STAR_UP = [10,20,40,80,160,320,640,1280]

mutation = [0.1,0.08,0.05,0.02,0.01,0.001]

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
soulbase = wl.csv_idmap("../AnotherWorldData/soulbase.csv")
equipmentbase = wl.csv_idmap("../AnotherWorldData/equipmentbase.csv")

buffbase = wl.csv_idmap("../AnotherWorldData/buffbase.csv")
wl.csv_param(buffbase,[ ["startlogic",[";",","]],["intervallogic",[";",","]],["endlogic",[";",","]] ])

skillbase = wl.csv_idmap("../AnotherWorldData/skillbase.csv")
wl.csv_param(skillbase,[ ["condition",[";",","]],["param",[","]] ])

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


