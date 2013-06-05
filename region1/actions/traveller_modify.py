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
	>>> info={'code':'traveller_modify','userid':'5','id':1,'name':'traveller','view':traveller.VIEW_ALL}
    >>> ret = do(info)
    >>> ret['rc'] == RetCode.USERID_NOTEXIST
    True
	"""
	ret = dict()
	
	obj = role.objects.filter(userid=info['userid'])
	if obj.count() != 0 :
		ret['rc'] = RetCode.PLAYER_NOTEXIST
		return ret
	
	traveller = obj.traveller_set.filter(id=info['id'])
	if traveller.count() != 0:
		ret['rc'] = RetCode.TRAVELLER_NOTEXIST
		return ret
	
	traveller.name = info['name']
	traveller.view = info['view']
	
	traveller.save()
	
	ret['rc'] = RetCode.OK
	return ret
