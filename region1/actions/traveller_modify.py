'''
Created on Apr 21, 2013

@author: w2moon
'''

from data.retcode import RetCode

arr = __file__.split('/')
appname = arr[len(arr)-3]
utils = None
exec("from "+appname+" import utils")

def do(info):
	"""
	traveller create
	>>> info={'code':'traveller_modify','userid':'5','id':1,'name':'traveller','gender':0,'age':0,'img':'tester','soul':0,'weapon':1,'cloth':2,'trinket':3}
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
		
	if info.has_key('weapon'):
		weapon = role.get_soul(info['weapon'])
		if weapon != None:
			if weapon.travellerid != 0 :
				oldtraveller = role.get_traveller(weapon.travellerid)
				if oldtraveller != None:
					oldtraveller.weaponid = 0
					oldtraveller.save()
			weapon.travellerid = traveller.id
			traveller.weaponid = info['weapon']
			weapon.save()
		
	if info.has_key('cloth'):
		cloth = role.get_soul(info['cloth'])
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
		trinket = role.get_soul(info['trinket'])
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
	return ret
