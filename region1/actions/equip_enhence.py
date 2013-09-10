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
    equip enhence
    >>> r = utils.create_role('12','12','tester')
    >>> r.save()
    >>> e1 = r.addEquip(1)
    >>> e2 = r.addEquip(1)
    >>> e3 = r.addEquip(1)
    >>> e4 = r.addEquip(1)
    >>> info={'code':'equip_enhence','userid':'12','equip':e1.id,'consume':[e2.id,e3.id,e4.id]}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.ENHENCE_NOT_ENOUGH_COPPER
    True
    >>> r.addCopper(10000)
    >>> r.save()
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.OK
    True
    >>> ret['equip']['level'] > 1
    True
    """
    ret = dict()
    ret['rc'] = RetCode.OK
    
    role = utils.get_role(info['userid'])
    if role == None :
        ret['rc'] = RetCode.USERID_NOTEXIST
        return ret
    
    target = role.getEquipment(info['equip'])
    if target == None:
        ret['rc'] = RetCode.EQUIP_NOTEXIST
        return ret
    
    if target.level >= data.rarityclass[data.equipmentbase[target.baseid]['rarityclass']]['maxlevel']:
        ret['rc'] = RetCode.ENHENCE_ALREADY_MAX_LEVEL
        return ret
    
    
    equips = []
    for k in info['consume']:
        e = role.getEquipment(k)
        if e == None or k == info['equip']:
            ret['rc'] = RetCode.EQUIP_NOTEXIST
            return ret
        equips.append(e)
    
    copper = 0
    totalexp = 0
    for e in equips:
        rarityclass = data.rarityclass[data.soulbase[e.baseid]['rarityclass']]
        copper += rarityclass['enhencecopper']
        totalexp += rarityclass['enhenceexp']
        
    if copper > role.copper:
        ret['rc'] = RetCode.ENHENCE_NOT_ENOUGH_COPPER
        return ret
    
    for e in equips:
        if e.travellerid != 0:
            traveller = role.getTraveller(e.travellerid)
            if traveller.weaponrid == e.id :
                traveller.weaponrid = 0
            elif traveller.weaponlid == e.id :
                traveller.weaponlid = 0
            elif traveller.clothid == e.id:
                traveller.clothid = 0
            elif traveller.trinketid == e.id:
                traveller.trinketid = 0
                
            traveller.save()
        e.delete()
        
    role.copper -= copper
    role.save()
    
    target.addExp(totalexp)
    ret['equip'] = target.pack()
    target.save()
    
    return ret
