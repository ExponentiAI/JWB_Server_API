"""server_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from medical_resources import views
from django.contrib import admin
from rest_framework.routers import DefaultRouter

router = routers.DefaultRouter()
router.register(r'Authentication', views.UserInfoViewSet)

# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
router.register(r'UserInfo', views.UserInfoViewSet)
router.register(r'Demand', views.DemandViewSet)
router.register(r'Material', views.MaterialViewSet)

# 使用自动URL路由连接我们的API。
# 另外，我们还包括支持浏览器浏览API的登录URL。
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework111')),
    # url(r'^hot/$', views.get_hot_info),
    url(r'^new/(?P<pindex>[0-9]+)/$', views.get_new_info),
    url(r'^me/(?P<pindex>[0-9]+)/$', views.get_me_info),
    url(r'^res_details/$', views.res_details),
    # 提交需求和供应
    url(r'^SupAndDem/$', views.SupAndDem, name="SupAndDem"),

    # 用户登录
    url(r'^UserLogin', views.UserLogin, name="UserLogin"),
    # 用户登录后，若为新用户（即数据库没有对应的open_id），则存库；否则，不存
    url(r'^UserRegister/$', views.UserRegister, name="UserRegister"),

    url(r'^storeList/(?P<pindex>[0-9]+)/$', views.store_list, name="store_list"),
]
