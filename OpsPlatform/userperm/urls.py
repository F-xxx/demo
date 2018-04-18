
from django.conf.urls import url
from . import views


app_name = 'userperm'
urlpatterns = [
    url(r'^$',views.dashboard,name='dashboard'),
    url(r'^verify_code$', views.check_code,name='verify_code'),
    url(r'^user_center/$',views.user_list,name='user_list'),
    url(r'^user_add/$',views.user_manage,name='user_add'),
    url(r'^audit/$',views.audit_log,name='audit'),

    url(r'^user_manage/(?P<uid>\d+)/(?P<action>[\w-]+)/$', views.user_manage, name='user_manage'),
    url(r'^group_list$',views.group_list,name='group_list'),
]
