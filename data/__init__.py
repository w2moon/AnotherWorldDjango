
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

travellerbase = wl.csv_idmap("../AnotherWorldData/travellerbase.csv")
soulbase = wl.csv_idmap("../AnotherWorldData/soulbase.csv")
equipmentbase = wl.csv_idmap("../AnotherWorldData/equipmentbase.csv")
buffbase = wl.csv_idmap("../AnotherWorldData/buffbase.csv")
skillbase = wl.csv_idmap("../AnotherWorldData/skillbase.csv")

def get_rolecfg():
    return rolecfg

def get_info(base,iid):
    if base.has_key(iid):
        return base[iid]
    return None
