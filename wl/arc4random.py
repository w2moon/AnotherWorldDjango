"""
"""
import math
import random as pyrandom

pool = {} #entropy pool starts empty
width = 256 #each RC4 output is 0 <= x < 256
chunks = 6 #at least six RC4 outputs for each double
digits = 52 #there are 52 significant digits in a double


startdenom = math.pow(width, chunks)
significance = math.pow(2,digits)
overflow = significance * 2
mask = width - 1


    
arc4_inst = None

#converts an array of charcodes to a string
def tostring(arr):
    tmp = []
    for d in arr:
        tmp.append(chr(d))
    return "".join(tmp)

def autoseed(seed):
    return ""+random.random()

def mixkey(seed,key):
    stringseed = str(seed)
    smear = 0
    j = 0
    while j < len(stringseed):
        idx = mask & j
        if key.has_key(idx) == False:
            key[idx] = 0
        smear = smear ^ (key[idx] * 19)
        key[idx] = mask & smear + ord(stringseed[j])
        j = j + 1
        
    return tostring(key)

def flatten(obj,depth = None):
    typ = type(obj)
    if typ == str:
        return obj
    else:
        return obj + '\0'
    

class ARC4:
    
    def __init__(self,key):
        t = 0
        keylen = len(key)
        me = self
        i = 0
        j = me.i = me.j = 0
        s = me.S = {}
    
        if keylen == 0:
            key = [keylen]
            keylen = keylen + 1
            
       
        
        while i < width:
            s[i] = i
            i = i + 1
        
        for i in xrange(width):
            t = s[i]
            j = mask & (j+key[i%keylen]+t)
            s[i] = s[j]
            s[j] = t
            
        self.g(width)
            
    def g(self,count):
        t = 0
        r = 0
        i = self.i
        j = self.j
        s = self.S
        while count > 0:
            count = count - 1
            i = mask & (i+1)
            t = s[i]
            j = mask & (j+t)
            s[i] = s[j]
            s[j] = t
            r = r*width + s[mask & (s[i]+s[j])]
            
        self.i = i
        self.j = j
        return r

def seed(seed = None,use_entropy = False):
    key = {}
    
    
    if not use_entropy:
        if seed != None:
            obj = seed
        else:
            obj = autoseed()
    else:
        obj = [seed,tostring(pool)]
    
    shortseed = mixkey(flatten(obj,3),key)
    
    global arc4_inst
    arc4_inst = ARC4(key)
            
    mixkey(tostring(arc4_inst.S),pool)
    
    return shortseed

def random():
    if arc4_inst == None:
        print("sysrand")
        return pyrandom.random()
    n = arc4_inst.g(chunks)
    d = startdenom
    x = 0
    
    while n < significance:
        n = (n+x)*width
        d = d*width
        x = arc4_inst.g(1)
        
    while n >= overflow:
        n = n/2
        d = d/2
        x = x >> 1
        
    return (n+x)/d
    

mixkey(pyrandom.random(),pool)