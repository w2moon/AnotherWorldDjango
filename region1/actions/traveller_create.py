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
	traveller create
	>>> info={'code':'traveller_create','userid':'5','name':'traveller','gender':0,'age':0,'img':'tester'}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.USERID_NOTEXIST
    True
    >>> info['userid'] = '1'
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.OK
    True
    >>> role = utils.get_role('1')
    >>> traveller = role.traveller_set.all()[0]
    >>> traveller.clothid
    2L
	"""
	ret = dict()
	
	role = utils.get_role(info['userid'])
	if role == None :
		ret['rc'] = RetCode.USERID_NOTEXIST
		return ret
	
	traveller = role.create_traveller()
		
	traveller.name = info['name']
	traveller.gender = info['gender']
	traveller.age = info['age']
	traveller.img = info['img']
	
	travellerbase = wl.get_rand(data.travellerbase)
	
	traveller.MaxHP = travellerbase['MaxHP']
	traveller.Attack = travellerbase['Attack']
	traveller.Defense = travellerbase['Defense']
	traveller.Heal = travellerbase['Heal']
	
	soulbase = data.get_info(data.soulbase,travellerbase['soulbaseid'])
	if soulbase != None:
		soul = role.create_soul(travellerbase['soulbaseid'])
		soul.travellerid = traveller.id
		traveller.soulid = soul.id
		soul.save()
		
	weaponbase = data.get_info(data.equipmentbase,travellerbase['weaponbaseid'])
	if weaponbase != None:
		weapon = role.create_equipment(travellerbase['weaponbaseid'])
		weapon.travellerid = traveller.id
		traveller.weaponid = weapon.id
		weapon.save()
		
	clothbase = data.get_info(data.equipmentbase,travellerbase['clothbaseid'])
	if clothbase != None:
		cloth = role.create_equipment(travellerbase['clothbaseid'])
		cloth.travellerid = traveller.id
		traveller.clothid = cloth.id
		cloth.save()
		
	trinketbase = data.get_info(data.equipmentbase,travellerbase['trinketbaseid'])
	if trinketbase != None:
		trinket = role.create_equipment(travellerbase['trinketbaseid'])
		trinket.travellerid = traveller.id
		traveller.trinketid = trinket.id
		trinket.save()
		
	traveller.save()
	
	ret['rc'] = RetCode.OK
	ret['traveller'] = traveller.pack()
	return ret
