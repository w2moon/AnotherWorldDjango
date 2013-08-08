"""
wl test
>>> tonumber("aaa")
'aaa'
>>> tonumber("123")
123
>>> tonumber("12.3")
12.3
>>> timezone_day_distance(timezone.datetime(2013,7,17,0,0) , timezone.datetime(2013,7,18,0,0))
-1
>>> timezone_day_distance(timezone.datetime(2013,7,17,0,0) , timezone.datetime(2013,7,17,0,0))
0
>>> timezone_day_distance(timezone.datetime(2013,7,17,0,0) , timezone.datetime(2013,7,16,0,0))
1
"""

import csv
import string
import random
import time
import math

from django.utils import timezone

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

def clamp(v,vmin,vmax):
    if v <= vmin:
        return vmin
    if v >= vmax:
        return vmax
    return v

def dict_merge(d1,d2):
    ret = {}
    for k in d1:
        ret[k] = d1[k] + d2[k]
        
    return ret

def timezone_day_distance(t1,t2):
    return int((time.mktime((t1.year,t1.month,t1.day,0,0,0,0,0,0)) - time.mktime((t2.year,t2.month,t2.day,0,0,0,0,0,0)))/86400)

def parse_param(param,tokens):
    if type(param) != str or param == '':
        return param
    
    if len(tokens) == 0:
        return tonumber(param)
    arr = param.split(tokens[0])
    if param[-1] == tokens[0]:
        arr.pop()
    
    for k in xrange(0,len(arr)):
        arr[k] = parse_param(arr[k],tokens[1:])
        
    return arr

def csv_param(c,m):
    for k,v in c.items():
        for i in m:
            v[i[0]] = parse_param(v[i[0]],i[1])
           
inner_id = 0 
def local_id():
    global inner_id
    inner_id += 1
    return inner_id

debug_enabled = False
debug_info = []        
def debug(*args):
    global debug_enabled
    global debug_info
    if debug_enabled:
        debug_info.append(args)
        
def debug_force(*args):
    global debug_info
    debug_info.append(args)
    
def debug_on():
    global debug_enabled
    debug_enabled = True
    
def debug_off():
    global debug_enabled
    debug_enabled = False
    
def get_debug():
    global debug_info
    s = ""
    for i in debug_info:
        s = s+str(i)
    return s