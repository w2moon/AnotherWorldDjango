
from django.conf.urls import patterns,url


arr = __file__.split('/')
appname = arr[len(arr)-2]

exec("import "+appname)
exec("from "+appname+" import views")
views = eval("reload("+appname+".views)")

urlpatterns = patterns('',
                       url(r'^(?P<sig>\w+)$',views.index,name='index'))