
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

rolecfg = wl.csv_cfg("../AnotherWorldData/rolecfg.csv")


lotterypool = wl.csv_idmap("../AnotherWorldData/lotterypool.csv")
wl.csv_param(lotterypool,[ ["pool",[";",","]] ])

submaps = wl.csv_idmap("../AnotherWorldData/submaps.csv")
wl.csv_param(submaps,[ ["reward",[";",","]],["stages",[","]] ])

enemy = wl.csv_idmap("../AnotherWorldData/enemy.csv")
stage = wl.csv_idmap("../AnotherWorldData/stage.csv")
wl.csv_param(stage,[ ["reward",[";",","]],["enemy",[";",","]] ])

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
