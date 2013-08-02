'''
Created on 2013-7-26

@author: pengw
'''
class functask(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.tasks = []
        
    def add(self,func,*args):
        self.tasks.insert(0,[func,args])
        
    def adds(self,calls):
        self.tasks = calls + self.tasks
        
    def addtail(self,func,*args):
        self.tasks.append([func,args])
        
    def remove(self,func):
        self.tasks.remove(func)
        
    def next(self):
        if len(self.tasks) > 0: 
            task = self.tasks[0]
            del self.tasks[0]
        else:
            task = None
        dt = None
        while task != None and dt == None:
            dt = task[0](*(task[1]))
            if dt == None:
                task = self.tasks[0]
                del self.tasks[0]
            
        return dt