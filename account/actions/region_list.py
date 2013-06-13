'''
Created on Apr 21, 2013

@author: w2moon
'''

from account.models import region
from data.retcode import RetCode

def do(info):
        """
        region_list test
        >>> r1 = region(name="region1",url="url",status=1,recommend=0)
        >>> r1.save()
        >>> info={'code':'region_list'}
        >>> ret = do(info)
        >>> ret['rc'] == RetCode.OK
        True
        >>> ret['regions']['region1']['url'] == "url"
        True
        """
        
        ret = dict()
        ret['rc'] = RetCode.OK
        regions = region.objects.all()
        
        ret['regions'] = {}
        for r in regions:
            ret['regions'][r.name] = {'url':r.url,'status':r.status,'recommend':r.recommend}
            #ret['regions'].append({'name':r.name,'url':r.url,'status':r.status,'recommend':r.recommend})
            
        

        return ret