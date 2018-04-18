
from django.conf.urls import url

from . import views



urlpatterns = [
    url(r'^list/$',views.asset_list,name='asset_list'),
    url(r'^add/$',views.asset_add,name='asset_add'),
    url(r'^server/add/$',views.server_add,name='server_add'),
    url(r'^chart/$',views.test_chart,name='chart'),
    url(r'^manage/(?P<nid>\d+)/(?P<action>[\w-]+)$',views.asset_manage,name='asset_manage'),
]
