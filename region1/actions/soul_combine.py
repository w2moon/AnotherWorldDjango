'''
Created on Apr 21, 2013

@author: w2moon
'''

from data.retcode import RetCode
import data

arr = __file__.split('/')
appname = arr[len(arr)-3]
utils = None
exec("from "+appname+" import utils")

def do(info):
    """
    soul combine
    >>> r = utils.create_role('8','8','tester')
    >>> r.save()
    >>> s1 = r.addSoul(1)
    >>> s2 = r.addSoul(2)
    >>> info={'code':'soul_combine','userid':'8','soulid1':s1.id,'soulid2':100}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.COMBINE_NOT_FOUND_SOUL
    True
    >>> info['soulid2'] = s2.id
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.COMBINE_NOT_ENOUGH_COPPER
    True
    >>> r.addCopper(10000)
    >>> r.save()
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.OK
    True
    >>> r.getSoul(s1.id)
    >>> r.getSoul(s2.id)
    >>> ret['soul'] != None
    True
    """
    ret = dict()
    
    ret['rc'] = RetCode.OK
    
    role = utils.get_role(info['userid'])
    if role == None :
        ret['rc'] = RetCode.USERID_NOTEXIST
        return ret
    
    s1 = role.getSoul(info['soulid1'])
    s2 = role.getSoul(info['soulid2'])
    
    if s1 == None or s2 == None:
        ret['rc'] = RetCode.COMBINE_NOT_FOUND_SOUL
    else:
        bid = data.get_combineid(s1.baseid,s2.baseid)
        if bid == None:
            ret['rc'] = RetCode.COMBINE_CAN_NOT_COMBINED
        else:
            rarityclass = data.rarityclass[data.soulbase[bid]['rarityclass']]
            
            if rarityclass['combinecopper'] > role.copper:
                ret['rc'] = RetCode.COMBINE_NOT_ENOUGH_COPPER
            else:
                role.copper -= rarityclass['combinecopper']
                role.save()
                                          
                if role.rand() < rarityclass['mutation']:
                    ids = data.mutation[rarityclass['id']]
                    bid = ids[int(len(ids)*role.rand())]
                    
                soul = role.addSoul(bid)
                
                if s1.travellerid != 0 and s2.travellerid != 0:
                    if role.slot5 == s1.travellerid:
                        traveller = role.getTraveller(s1.travellerid)
                        s1.travellerid = 0
                        traveller.soulid = soul.id
                        soul.travellerid = traveller.id
                        traveller.save()
                        soul.save()
                    elif role.slot5 == s2.travellerid:
                        traveller = role.getTraveller(s2.travellerid)
                        s2.travellerid = 0
                        traveller.soulid = soul.id
                        soul.travellerid = traveller.id
                        traveller.save()
                        soul.save()
                    else:
                        traveller = role.getTraveller(s1.travellerid)
                        s1.travellerid = 0
                        traveller.soulid = soul.id
                        soul.travellerid = traveller.id
                        traveller.save()
                        soul.save()
                        
                        traveller = role.getTraveller(s2.travellerid)
                        s2.travellerid = 0
                        traveller.soulid = 0
                        traveller.save()
                        
                        
                elif s1.travellerid != 0:
                    traveller = role.getTraveller(s1.travellerid)
                    s1.travellerid = 0
                    traveller.soulid = soul.id
                    soul.travellerid = traveller.id
                    traveller.save()
                    
                elif s2.travellerid != 0:
                    traveller = role.getTraveller(s2.travellerid)
                    s2.travellerid = 0
                    traveller.soulid = soul.id
                    soul.travellerid = traveller.id
                    traveller.save()
                
                s1.delete()
                s2.delete()
                
                ret['soul'] = soul.pack()
       
    return ret
