'''
Created on Apr 21, 2013

@author: w2moon
'''

from data.retcode import RetCode

arr = __file__.split('/')
appname = arr[len(arr)-3]
utils = None
exec("from "+appname+" import utils")

import data
def do(info):
	"""
	traveller create
	>>> info={'code':'traveller_modify','userid':'5','id':1,'name':'traveller','gender':0,'age':0,'img':'tester','soul':0,'weaponr':1,'weaponl':1,'cloth':2,'trinket':3}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.USERID_NOTEXIST
    True
	"""
	ret = dict()
	
	role = utils.get_role(info['userid'])
	if role == None :
		ret['rc'] = RetCode.USERID_NOTEXIST
		return ret
	
	traveller = role.get_traveller(info['id'])
	if traveller == None:
		ret['rc'] = RetCode.TRAVELLER_NOTEXIST
		return ret
	
	if info.has_key('name'):
		traveller.name = info['name']
		
	if info.has_key('gender'):
		traveller.gender = info['gender']
		
	if info.has_key('age'):
		traveller.age = info['age']
		
	if info.has_key('img'):
		traveller.img = info['img']
		
	if info.has_key('soul'):
		soul = role.get_soul(info['soul'])
		if soul != None:
			if soul.travellerid != 0 :
				oldtraveller = role.get_traveller(soul.travellerid)
				if oldtraveller != None:
					oldtraveller.soulid = 0
					oldtraveller.save()
			soul.travellerid = traveller.id
			traveller.soulid = info['soul']
			soul.save()
		
	if info.has_key('weaponr'):
		weaponr = role.getEquipment(info['weaponr'])
		if weaponr != None:
			tpy = weaponr.getBase()['type']
			if tpy != data.WEAPON_OFFHAND:
				if weaponr.travellerid != 0 :
					oldtraveller = role.get_traveller(weaponr.travellerid)
					if oldtraveller != None:
						oldtraveller.weaponrid = 0
						oldtraveller.save()
				if traveller.weaponrid != 0:
					oldweapon = role.getEquipment(traveller.weaponrid)
					oldweapon.travellerid = 0
					oldweapon.save()
					
				if tpy == data.WEAPON_TWOHAND and traveller.weaponlid != 0:
					oldweapon = role.getEquipment(traveller.weaponlid)
					oldweapon.travellerid = 0
					traveller.weaponlid = 0
					oldweapon.save()
					
				weaponr.travellerid = traveller.id
				traveller.weaponrid = info['weaponr']
				weaponr.save()
		else:
			if traveller.weaponrid != 0:
				oldweapon = role.getEquipment(traveller.weaponrid)
				oldweapon.travellerid = 0
				oldweapon.save()
			traveller.weaponrid = 0
			
	if info.has_key('weaponl'):
		weaponl = role.getEquipment(info['weaponl'])
		if weaponl != None:
			tpy = weaponl.getBase()['type']
			if tpy == data.WEAPON_OFFHAND or tpy == data.WEAPON_ONEHAND:
				if traveller.weaponrid != 0:
					oldweapon = role.getEquipment(traveller.weaponlid)
					oldweapon.travellerid = 0
					traveller.weaponlid = 0
					oldweapon.save()
					
				if weaponl.travellerid != 0 :
					oldtraveller = role.get_traveller(weaponl.travellerid)
					if oldtraveller != None:
						oldtraveller.weaponlid = 0
						oldtraveller.save()
						
				if traveller.weaponrid != 0:
					oldweapon = role.getEquipment(traveller.weaponrid)
					if oldweapon.getBase()['type'] == data.WEAPON_TWOHAND:
						oldweapon.travellerid = 0
						traveller.weaponrid = 0
						oldweapon.save()
					
				weaponl.travellerid = traveller.id
				traveller.weaponlid = info['weaponl']
				weaponl.save()
		else:
			if traveller.weaponlid != 0:
				oldweapon = role.getEquipment(traveller.weaponlid)
				oldweapon.travellerid = 0
				oldweapon.save()
			traveller.weaponlid = 0
		
	if info.has_key('cloth'):
		cloth = role.getEquipment(info['cloth'])
		if cloth != None:
			if cloth.travellerid != 0 :
				oldtraveller = role.get_traveller(cloth.travellerid)
				if oldtraveller != None:
					oldtraveller.clothid = 0
					oldtraveller.save()
			cloth.travellerid = traveller.id
			traveller.clothid = info['cloth']
			cloth.save()
		
	if info.has_key('trinket'):
		trinket = role.getEquipment(info['trinket'])
		if trinket != None:
			if trinket.travellerid != 0 :
				oldtraveller = role.get_traveller(trinket.travellerid)
				if oldtraveller != None:
					oldtraveller.clothid = 0
					oldtraveller.save()
			trinket.travellerid = traveller.id
			traveller.trinketid = info['trinket']
			trinket.save()
	
	traveller.save()
	
	ret['rc'] = RetCode.OK
	ret['traveller'] = traveller.pack()
	return ret
