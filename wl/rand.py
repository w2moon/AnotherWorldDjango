'''
Created on 2013-7-16

@author: pengw
'''
import math
import random
import json

class rand(object):
    '''
    classdocs
    '''

    def __init__(self,pool = {},width = 256,chunks = 6,digits = 52):
        '''
        Constructor
        '''
        self.S = None
        
        self.pool = pool #entropy pool starts empty
        self.width = width #each RC4 output is 0 <= x < 256
        self.chunks = chunks #at least six RC4 outputs for each double
        self.digits = digits #there are 52 significant digits in a double
    
    
        self.startdenom = math.pow(self.width, self.chunks)
        self.significance = math.pow(2,self.digits)
        self.overflow = self.significance * 2
        self.mask = self.width - 1
        
        self.mixkey(random.random(),self.pool)
        
    def arc4(self,key):
        t = 0
        keylen = len(key)
        me = self
        i = 0
        j = me.i = me.j = 0
        s = me.S = {}
    
        if keylen == 0:
            key = [keylen]
            keylen = keylen + 1
            
       
        
        while i < self.width:
            s[i] = i
            i = i + 1
        
        for i in xrange(self.width):
            t = s[i]
            j = self.mask & (j+key[i%keylen]+t)
            s[i] = s[j]
            s[j] = t
            
        self.g(self.width)
        
    def g(self,count):
        t = 0
        r = 0
        i = self.i
        j = self.j
        s = self.S
        while count > 0:
            count = count - 1
            i = self.mask & (i+1)
            t = s[i]
            j = self.mask & (j+t)
            s[i] = s[j]
            s[j] = t
            r = r*self.width + s[self.mask & (s[i]+s[j])]
            
        self.i = i
        self.j = j
        return r
    
    def pack_str(self):
        if self.S == None:
            return ""
        o = self.pack()
        return json.dumps(o);
    
    def unpack_str(self,s):
        if s == "":
            return
        o = json.loads(s)
        self.unpack(o)
        
    def pack(self):
        s = []
        for k in xrange(len(self.S)):
            s.append(self.S[k])
        return [self.i,self.j,s,self.mask,self.width,self.chunks,self.significance,self.overflow,self.startdenom]
    
    def unpack(self,o):
        self.i = o[0]
        self.j = o[1]
        s = o[2]
        self.S = {}
        for k in xrange(len(s)):
            self.S[k] = s[k]
        self.mask = o[3]
        self.width = o[4]
        self.chunks = o[5]
        self.significance = o[6]
        self.overflow = o[7]
        self.startdenom = o[8]
    
    #converts an array of charcodes to a string
    def tostring(self,arr):
        tmp = []
        for d in arr:
            tmp.append(chr(d))
        return "".join(tmp)
    
    def autoseed(self,seed):
        return ""+random.random()
    
    def mixkey(self,seed,key):
        stringseed = str(seed)
        smear = 0
        j = 0
        while j < len(stringseed):
            idx = self.mask & j
            if key.has_key(idx) == False:
                key[idx] = 0
            smear = smear ^ (key[idx] * 19)
            key[idx] = self.mask & smear + ord(stringseed[j])
            j = j + 1
            
        return self.tostring(key)
    
    def flatten(self,obj,depth = None):
        typ = type(obj)
        if typ == str:
            return obj
        else:
            return obj + '\0'
        
    def seed(self,seed = None,use_entropy = False):
        key = {}
        
        
        if not use_entropy:
            if seed != None:
                obj = seed
            else:
                obj = self.autoseed()
        else:
            obj = [seed,self.tostring(self.pool)]
        
        shortseed = self.mixkey(self.flatten(obj,3),key)
        
        self.arc4(key)
                
        self.mixkey(self.tostring(self.S),self.pool)
        
        return shortseed
    
    def random(self):
        if self.S == None:
            return random.random()
        n = self.g(self.chunks)
        d = self.startdenom
        x = 0
        
        while n < self.significance:
            n = (n+x)*self.width
            d = d*self.width
            x = self.g(1)
            
        while n >= self.overflow:
            n = n/2
            d = d/2
            x = x >> 1
            
        return (n+x)/d
        