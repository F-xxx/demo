
from django.conf.urls import url
from . import views

from rest_framework.urlpatterns import format_suffix_patterns
# router = routers.DefaultRouter()
#
# router.register(r'assets',views.AssetServerViewSet)


# urlpatterns = [
#     url(r'',include(router.urls)),
#     url(r'asset/server',include(router.urls)),
# ]


urlpatterns = [
    url(r'^asset/list/$',views.asset_list),
    url(r'^server/list/$',views.server_list),
    url(r'^user/list/$',views.user_list),
    url(r'^asset/(?P<pk>[0-9]+)/$',views.asset_detail),
    url(r'^server/(?P<pk>[0-9]+)/$',views.server_detail),
    url(r'^user/(?P<pk>[0-9]+)/$',views.user_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
