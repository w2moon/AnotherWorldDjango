'''
Created on 2013-7-17

@author: pengw
'''
from role import role
from player import player

import state
import wl
import data

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





import random as sysrand
    

class battlefield(object):
    '''
    classdocs
    '''
    
    def rand(self):
        return sysrand.random()
    
    
    def select_left(self,objs,nature_type,num,out_array,selecthero,needalive):
        for k in xrange(0,len(objs)):
            if k == data.HERO_IDX:
                continue
            if num == 0:
                break
            o = objs[k]
            if o == None:
                continue
            if (needalive and not o.isDead()) or (not needalive and o.isDead()):
                out_array.append(o)
                num -= 1
                
        if selecthero and objs[data.HERO_IDX] != None and (len(out_array) == 0 or num < 0):
            out_array.append(objs[data.HERO_IDX])
                
    def select_right(self,objs,nature_type,num,out_array,selecthero,needalive):
        for k in xrange(len(objs)-1,-1,-1):
            if k == data.HERO_IDX :
                continue
            if num == 0:
                break
            o = objs[k]
            if o == None:
                continue
            if (needalive and not o.isDead()) or (not needalive and o.isDead()):
                out_array.append(o)
                num -= 1
                
        if selecthero and objs[data.HERO_IDX] != None and (len(out_array) == 0 or num < 0):
            out_array.append(objs[data.HERO_IDX])
    
    def select_random(self,objs,nature_type,num,out_array,selecthero,needalive):
        arr = []    
        for k in xrange(0,len(objs)):    
            o = objs[k]
            if o == None:
                continue
            if (needalive and not o.isDead()) or (not needalive and o.isDead()):
                if k != data.HERO_IDX or selecthero:
                    arr.append(o)
            
        while len(arr) > 0 and num > 0:
            k = int(self.rand()*len(arr))
            out_array.append(arr[k])
            del arr[k]
            num -= 1
            
    def select_lowesthp(self,objs,nature_type,num,out_array,selecthero,needalive):
        if num == -1:
            for o in objs:
                if o == None:
                    continue
                if not o.isDead():
                    if selecthero or o != objs[data.HERO_IDX]:
                        out_array.append(o)
        else:
            for o in objs:
                if o == None:
                    continue
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
        
    def getWarriors(self):
        return self.warriors

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
            for k in xrange(0,len(warriors)-1):
                if warriors[k] == actor:
                    if enemywarriors[k] != None and ( (needalive and not enemywarriors[k].isDead()) or (not needalive and enemywarriors[k].isDead()) ):
                        target = enemywarriors[k]
                break
            if target == None:
                for k in xrange(0,len(enemywarriors)):
                    if enemywarriors[k] != None and ( (needalive and not enemywarriors[k].isDead()) or (not needalive and enemywarriors[k].isDead()) ):
                        target = enemywarriors[k]
                        break
            
            targets.append(target)
        else:
            for p in self.players:
                if p != player:
                    self.nature_select(p.getWarriors(), nature_type, target_num, targets, True, needalive)
                    if target_num != -1 and len(targets) >= target_num:
                        break 
        
        return targets
    
    def target_ally(self,player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets):
        targets = []
        for p in self.players:
            if p == player:
                self.nature_select(p.getWarriors(), nature_type, target_num, targets, True, needalive)
                if target_num != -1 and len(targets) >= target_num:
                    break
        return targets
    
    def target_all(self,player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets):
        targets = []
        
        for w in self.warriors:
            if w != None and ( (needalive and not w.isDead()) or (not needalive and w.isDead()) ):
                targets.append(w)
        return targets
    
    def target_self(self,player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets):
        targets = []
        
        if (needalive and not actor.isDead()) or (not needalive and actor.isDead()):
            targets.append(actor)
            
        return targets
    
    def target_onlyallyfront(self,player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets):
        targets = []
        
        for p in self.players:
            if p == player:
                self.nature_select(p.getWarriors(), nature_type, target_num, targets, False, needalive)
                if target_num != -1 and len(targets) >= target_num:
                    break
                
        return targets
    
    def target_onlyallyhero(self,player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets):
        targets = []
        
        for p in self.players:
            if p == player:
                hero = p.getWarriors()[data.HERO_IDX]
                if hero != None and ((needalive and not hero.isDead()) or (not needalive and hero.isDead())):
                    targets.append(hero)
                    
                
        return targets
    
    def target_onlyenemyfront(self,player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets):
        targets = []
        
        for p in self.players:
            if p != player:
                self.nature_select(p.getWarriors(), nature_type, target_num, targets, False, needalive)
                if target_num != -1 and len(targets) >= target_num:
                    break
                
        return targets
    
    def target_onlyenemyhero(self,player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets):
        targets = []
        
        for p in self.players:
            if p != player:
                hero = p.getWarriors()[data.HERO_IDX]
                if hero != None and ((needalive and not hero.isDead()) or (not needalive and hero.isDead())):
                    targets.append(hero)
                    
                
        return targets
    
    def target_eventtrigger(self,player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets):
        targets = []
        
        if (needalive and not trigger.isDead()) or (not needalive and trigger.isDead()):
            targets.append(trigger)
        
        return targets
    
    def target_eventtargets(self,player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets):
        targets = []
        
        for w in event_targets:
            if (needalive and not w.isDead()) or (not needalive and w.isDead()):
                targets.append(w)
        
        return targets
      
    
    def select_target(self,player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets):
        target_funcs = {
                        'enemy':lambda:self.target_enemy(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'ally':lambda:self.target_ally(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'all':lambda:self.target_all(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'self':lambda:self.target_self(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'onlyallyfront':lambda:self.target_onlyallyfront(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'onlyallyhero':lambda:self.target_onlyallyhero(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'onlyenemyfront':lambda:self.target_onlyenemyfront(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'onlyenemyhero':lambda:self.target_onlyenemyhero(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'eventtrigger':lambda:self.target_eventtrigger(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        'eventtarget':lambda:self.target_eventtarget(player,actor,target_type,target_num,nature_type,needalive,trigger,event_targets),
                        }
        return target_funcs[target_type]()

    def __init__(self,info,owner):
        '''
        Constructor
        '''
        self.info = info
        self.owner = owner
        self.functask = wl.functask.functask()
        roles = [role(owner),role.create_from_enemy(info['enemy'])]
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
            if w != None:
                w.battle_init()
                self.warriors.append(w)
            
    def on_warrior_event(self,*args):
        for w in self.warriors:
            if w != None:
                w.on_event(*args)
            
    def delayupdate(self,dt):
        self.turn_process()
    
    def start(self):
        self.turn = 1
        self.state = state.state_normal
        
    def turn_process(self):
        dt = self.functask.next()
        if dt != None:
            #self.delayupdate(dt)
            return
        self.state(self)
        #self.delayupdate(self.state(self))
        
    def isFinished(self):
        return self.state == state.state_finish
        
        
            
        