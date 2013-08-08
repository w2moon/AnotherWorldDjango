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
	ret['traveller'] = traveller.pack()
	return ret
