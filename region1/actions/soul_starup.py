'''
Created on Apr 21, 2013

@author: w2moon
'''

from data.retcode import RetCode
import data
import wl

arr = __file__.split('/')
appname = arr[len(arr)-3]
utils = None
exec("from "+appname+" import utils")

def do(info):
    """
    soul starup
    >>> r = utils.create_role('7','7','tester')
    >>> r.save()
    >>> s1 = r.addSoul(1)
    >>> s2 = r.addSoul(2)
    >>> s3 = r.addSoul(1)
    >>> s1.level = data.get_info(data.rarityclass,data.soulbase[s1.baseid]['rarityclass'])['maxlevel']
    >>> s2.level = data.get_info(data.rarityclass,data.soulbase[s2.baseid]['rarityclass'])['maxlevel']
    >>> s1.save()
    >>> s2.save()
    >>> r.save()
    >>> info={'code':'soul_starup','userid':'7','soulid1':s1.id,'soulid2':s2.id}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.STARUP_NOT_SAME_SOUL
    True
    >>> info['soulid2'] = s1.id
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.STARUP_NOT_FOUND_SOUL
    True
    >>> info['soulid2'] = s3.id
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.STARUP_NOT_ENOUGH_COPPER
    True
    >>> r.addCopper(10000)
    >>> r.save()
    >>> s3.star = 10
    >>> s3.save()
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.STARUP_ALREADY_MAX_STAR
    True
    >>> s3.star = 0
    >>> s3.save()
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.STARUP_NOT_FULL_LEVEL
    True
    >>> s3.level = data.get_info(data.rarityclass,data.soulbase[s3.baseid]['rarityclass'])['maxlevel']
    >>> s3.save()
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.OK
    True
    >>> r.getSoul(s1.id).star
    1L
    >>> r.getSoul(s3.id)
    """
    ret = dict()
    
    role = utils.get_role(info['userid'])
    if role == None :
        ret['rc'] = RetCode.USERID_NOTEXIST
        return ret
    
    if info['soulid1'] == info['soulid2']:
        ret['rc'] = RetCode.STARUP_NOT_FOUND_SOUL
        return ret
    s1 = role.getSoul(info['soulid1'])
    s2 = role.getSoul(info['soulid2'])
    
    ret['rc'] = RetCode.OK
    if s1 != None and s2 != None:
        if s1.baseid != s2.baseid :
            ret['rc'] = RetCode.STARUP_NOT_SAME_SOUL
        else:
            rarityclass = data.rarityclass[data.soulbase[s1.baseid]['rarityclass']]
            if rarityclass['starupcopper'][s1.star] > role.copper:
                ret['rc'] = RetCode.STARUP_NOT_ENOUGH_COPPER
            elif s1.star >= len(rarityclass['starupcopper']) or s2.star >= len(rarityclass['starupcopper']):
                ret['rc'] = RetCode.STARUP_ALREADY_MAX_STAR
            elif s1.level == rarityclass['maxlevel'] and s2.level == rarityclass['maxlevel']:
                role.copper -= rarityclass['starupcopper'][s1.star]
                s1.star = wl.clamp(s1.star + s2.star + 1,0,len(rarityclass['starupcopper']))
                s1.exp = 0
                s1.level = 0
                if s2.travellerid != 0:
                    traveller = role.getTraveller(s2.travellerid)
                    s2.travellerid = 0
                    traveller.soulid = 0
                    traveller.save()
                s2.delete()
                s1.save()
                
            else:
                ret['rc'] = RetCode.STARUP_NOT_FULL_LEVEL
            
    else:
        ret['rc'] = RetCode.STARUP_NOT_FOUND_SOUL
    
    
    
    return ret
