from gameobject import gameobject

class buff(gameobject):
    def __init__(self,warrior,battlefield,buffbase):
        self.warrior = warrior
        self.battlefield = battlefield
        self.buffbase = buffbase
        
        self.triggers = []
        self.stack = 1
        
        self.resttime = self.buffbase['duration'] + 1
        self.intervaltime = self.buffbase['interval']
        
        self.addTask(self.on_start)
        
    def getId(self):
        return self.buffbase['id']
    
    def getBase(self):
        return self.buffbase
    
    def addLink(self,trigger):
        self.triggers.append(trigger)
        
    def removeLink(self,trigger):
        self.triggers.remove(trigger)
        
    def hasLink(self,trigger):
        for t in self.triggers:
            if t == trigger:
                return True
        return False
    
    def isCleared(self):
        return len(self.triggers) == 0
    
    def destroy(self):
        self.addTask(self.on_end)
        
    def getStack(self):
        return self.stack
    
    def doLogic(self,logic):
        if logic == "":
            return
        
        for l in logic:
            arr = l[1:]
            try:
                getattr(self.warrior,l[0])(*arr)
            except:
                arr.append(self.triggers[0])
                getattr(self.warrior,l[0])(*arr)
            
    def setStack(self,s):
        if s >= self.stack:
            return
        
        #for i in xrange(1,s-self.stack+1):
        #    self.doLogic(self.buffbase['startlogic'])
        self.stack = s
        
    def update(self):
        if self.buffbase['interval'] != -1:
            self.intervaltime -= 1
            if self.intervaltime == 0:
                self.intervaltime = self.buffbase.interval
                self.addTask(self.on_interval)
            
        if self.buffbase['duration'] != -1:
            self.resttime -= 1
            if self.resttime == 0:
                self.addTask(self.on_end)
                return True #to delete
        
        return False
    
    def refreshDuration(self):
        self.resttime = self.buffbase['duration'] + 1
        
    def on_start(self):
        self.doLogic(self.buffbase.startlogic)
        
    def on_interval(self):
        self.doLogic(self.buffbase.intervallogic)
        
    def on_end(self):
        self.doLogic(self.buffbase.endlogic)
        
    def addTask(self,func):
        
        self.battlefield.addTask(func)