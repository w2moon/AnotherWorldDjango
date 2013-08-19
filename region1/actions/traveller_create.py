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
	>>> info={'code':'traveller_create','userid':'5','name':'traveller','gender':0,'age':0,'img':'tester','ishuman':1}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.USERID_NOTEXIST
    True
    >>> info['userid'] = '1'
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.OK
    True
    >>> role = utils.get_role('1')
    >>> traveller = role.traveller_set.all()[0]
    >>> traveller.weaponrid != 0
    True
	"""
	ret = dict()
	
	role = utils.get_role(info['userid'])
	if role == None :
		ret['rc'] = RetCode.USERID_NOTEXIST
		return ret
	
	
	travellerbase = wl.get_rand(data.travellerbase)
	traveller = role.addTraveller(info,travellerbase)
		
	
	ret['rc'] = RetCode.OK
	if traveller != None:
		ret['traveller'] = traveller.pack()
		if traveller.soulid != 0:
			ret['soul'] = role.getSoul(traveller.soulid).pack()
		ret['equips'] = []
		if traveller.weaponrid != 0:
			ret['equips'].append( role.getEquipment(traveller.weaponrid).pack() )
		if traveller.weaponlid != 0:
			ret['equips'].append( role.getEquipment(traveller.weaponlid).pack() )
		if traveller.clothid != 0:
			ret['equips'].append( role.getEquipment(traveller.clothid).pack() )
		if traveller.trinketid != 0:
			ret['equips'].append( role.getEquipment(traveller.trinketid).pack() )
			
		if role.slot5 == 0:
			role.slot5 = traveller.id
			role.name = traveller.name
			if role.level == 0:
				role.level = 1
			role.save()
	return ret
