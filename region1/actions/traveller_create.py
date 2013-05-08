'''
Created on Apr 21, 2013

@author: w2moon
'''
from django.utils import timezone


from retcode import RetCode

arr = __file__.split('/')
appname = arr[len(arr)-3]

exec("import "+appname)
role = eval("reload("+appname+".models)").role

def do(info):
	ret = dict()
	
	return ret