'''
Created on Apr 21, 2013

@author: w2moon
'''

from data.retcode import RetCode

arr = __file__.split('/')
appname = arr[len(arr)-3]

exec("import "+appname)
role = eval("reload("+appname+".models)").role

def do(info):
	"""
	traveller create
	>>> info={'code':'traveller_create','userid':'5','img':'tester'}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.USERID_NOTEXIST
    True
	"""
	ret = dict()
	
	obj = role.objects.filter(userid=info['userid'])
	if obj.count() == 0 :
		ret['rc'] = RetCode.PLAYER_NOTEXIST
		return ret
	else:
		obj = obj[0]
	
	traveller = obj.traveller_set.create()
	
	traveller.img = info['img']
	
	traveller.save()
	
	ret['rc'] = RetCode.OK
	ret['traveller'] = traveller.pack()
	return ret
