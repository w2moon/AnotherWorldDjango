
from django.conf.urls import patterns,url

from account import views

urlpatterns = patterns('',
                       url(r'^(?P<sig>\w+)$',views.index,name='index'))