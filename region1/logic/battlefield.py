'''
Created on 2013-7-17

@author: pengw
'''
from role import role
from player import player

import state
import wl

def sort_hp(t1,t2):
    h1 = t2.getHP()
    h2 = t1.getHP()
    if h2 > h1:
        return 1
    elif h1 == h2:
        return 0
    else:
        return -1

random = 0
lowesthp = 1
opposite = 2
left = 3
right = 4






    

class battlefield(object):
    '''
    classdocs
    '''
    
    def rand(self):
        return 0
    
    
    def select_left(self,objs,nature_type,num,out_array,selecthero,needalive):
        for k in xrange(0,len(objs)):
            if k == 0:
                continue
            if num == 0:
                break
            o = objs[k]
            if (needalive and not o.isDead()) or (not needalive and o.isDead()):
                out_array.append(o)
                num -= 1
                
        if selecthero and (len(out_array) == 0 or num < 0):
            out_array.push(objs[0])
                
    def select_right(self,objs,nature_type,num,out_array,selecthero,needalive):
        for k in xrange(len(objs)-1,-1,-1):
            if k == 0:
                continue
            if num == 0:
                break
            o = objs[k]
            if (needalive and not o.isDead()) or (not needalive and o.isDead()):
                out_array.append(o)
                num -= 1
                
        if selecthero and (len(out_array) == 0 or num < 0):
            out_array.push(objs[0])
    
    def select_random(self,objs,nature_type,num,out_array,selecthero,needalive):
        arr = []    
        for k in xrange(0,len(objs)):    
            o = objs[k]
            if (needalive and not o.isDead()) or (not needalive and o.isDead()):
                if k != 0 or selecthero:
                    arr.append(o)
            
        while len(arr) > 0 and num > 0:
            k = int(self.rand()*len(arr))
            out_array.append(arr[k])
            del arr[k]
            num -= 1
            
    def select_lowesthp(self,objs,nature_type,num,out_array,selecthero,needalive):
        if num == -1:
            for o in objs:
                if not o.isDead():
                    out_array.append(o)
        else:
            for o in objs:
                if o.isDead():
                    continue
                if len(out_array) < num:
                    out_array.append(o)
                else:
                    if num > 1:
                        out_array.sort(sort_hp)
                        for a in out_array:
                            if o.getHP() < a.getHP():
                                out_array[0] = o
                                break
                    else:
                        out_array[0] = o
        

    def nature_select(self,objs,nature_type,num,out_array,selecthero,needalive):
        select_funcs = {
                left:lambda:self.select_left(objs,nature_type,num,out_array,selecthero,needalive),
                right:lambda:self.select_right(objs,nature_type,num,out_array,selecthero,needalive),
                random:lambda:self.select_random(objs,nature_type,num,out_array,selecthero,needalive),
                lowesthp:lambda:self.select_lowesthp(objs,nature_type,num,out_array,selecthero,needalive),
               # opposite:lambda:self.select_opposite(objs,nature_type,num,out_array,selecthero,needalive),
                }
        return select_funcs[nature_type]()
    
    def target_enemy(self,player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets):
        targets = []
        
        if nature_type == 'opposite':
            target = None
            enemywarriors = None
            warriors = player.getWarriors()
            for p in self.players:
                if p != player:
                    enemywarriors = p.getWarriors()
                    break
            for w in warriors:
                if w == actor:
                    if (needalive and not ) or ():
                        target = ew
                break
        else:
            for p in self.players:
                if p != player:
                    self.nature_select(p.getWarriors(), nature_type, target_num, targets, True, needalive)
        
        return targets
    
    def select_target(self,player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets):
        target_funcs = {
                        'enemy':lambda:self.target_enemy(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'ally':lambda:self.target_enemy(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'all':lambda:self.target_enemy(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'self':lambda:self.target_enemy(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'onlyallyfront':lambda:self.target_enemy(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'onlyallyhero':lambda:self.target_enemy(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'onlyenemyfront':lambda:self.target_enemy(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'onlyenemyhero':lambda:self.target_enemy(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'eventtrigger':lambda:self.target_enemy(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'eventtarget':lambda:self.target_enemy(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        }
        
        return target_funcs[target_type]()

    def __init__(self,info,owner):
        '''
        Constructor
        '''
        self.info = info
        self.owner = owner
        
        self.functask = wl.functask()
        
        roles = [role(owner),role.create_from_enemy(info.enemy)]
        self.initBattle(roles)
        self.start()
        
    def addTask(self,*args):
        self.functask.add(*args)
        
    def addTaskTail(self,*args):
        self.functask.addtail(*args)
        
    def addTasks(self,*args):
        self.functask.adds(*args)
        
        
    def initBattle(self,roles):
        self.players = []
        self.warriors = []
        for r in roles:
            p = player(r,self)
            self.players.append(p)
            self.init_role(p)
            
    def init_role(self,p):
        for w in p.getWarriors():
            w.battle_init()
            
    def on_warrior_event(self,*args):
        for w in self.warriors:
            w.on_event(*args)
            
    def delayupdate(self,t):
        pass
    
    def start(self):
        self.turn = 1
        self.state = state.state_normal
        
    def turn_process(self):
        dt = self.functask.next()
        if dt != None:
            return
        self.state(self)
        
            
        