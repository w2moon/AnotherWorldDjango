'''
Created on Apr 21, 2013

@author: w2moon
'''

from account.models import region
from retcode import RetCode

def do(info):
        """
        region_list test
        >>> info={'code':'region_list','ip':'127.0.0.1'}
        >>> ret = do(info)
        >>> ret['rc'] == RetCode.OK
        True
        """
        
        ret = dict()
        ret['rc'] = RetCode.OK
        regions = region.objects.all()
        
        ret['regions'] = []
        for r in regions:
            ret['regions'].push({'name':r.name,'url':r.url,'status':r.status,'recommend':r.recommend})
            
        

        return ret