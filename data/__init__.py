
"""
basedata test 
>>> roletemplate[1]['id']
1
>>> soulbase[1]['id']
1
>>> equipbase[1]['id']
1
>>> buffbase[1000]['id']
1000
>>> skillbase[1000]['id']
1000
"""

import wl

roletemplate = wl.csv_idmap("../AnotherWorldData/roletemplate.csv")
soulbase = wl.csv_idmap("../AnotherWorldData/soulbase.csv")
equipbase = wl.csv_idmap("../AnotherWorldData/equipmentbase.csv")
buffbase = wl.csv_idmap("../AnotherWorldData/buffbase.csv")
skillbase = wl.csv_idmap("../AnotherWorldData/skillbase.csv")