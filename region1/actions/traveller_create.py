'''
Created on Apr 21, 2013

@author: w2moon
'''

from retcode import RetCode

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
	if obj.count() != 0 :
		ret['rc'] = RetCode.PLAYER_NOTEXIST
		return ret
	
	ret['rc'] = RetCode.OK
	
	return ret