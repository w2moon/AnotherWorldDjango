"""
wl test
>>> tonumber("aaa")
'aaa'
>>> tonumber("123")
123
>>> tonumber("12.3")
12.3
"""

import csv
import string
import random

def tonumber(v):
    if type(v) != str or v == "":
        return v
    try:
        if v.find(".") == -1:
            return string.atoi(v);
        else:
            return string.atof(v);
    except:
        return v
    

def csv_idmap(filepath):
    ret = {}
    cf = file(filepath,'rb')
    reader = csv.reader(cf)
    nameline = None
    for line in reader:
        if nameline == None:
            nameline = line
        else:
            obj = {}
            idx = 0
            for name in nameline:
                obj[name] = tonumber(line[idx])
                idx = idx + 1
            ret[tonumber(line[0])] = obj
                
    cf.close()
    return ret

def csv_cfg(filepath):
    ret = {}
    cf = file(filepath,'rb')
    reader = csv.reader(cf)
    for line in reader:
        ret[line[0]] = tonumber(line[1])
                
    cf.close()
    return ret

def get_rand(dicobj):
    r = random.random()
    v = 0
    for k in dicobj:
        v = v + dicobj[k]['rate']
        if r < v:
            return dicobj[k]
    return None
