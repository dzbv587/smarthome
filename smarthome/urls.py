"""
URL configuration for smarthome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import TokenRefreshView


from user.views import UserViewSet, MyTokenObtainPairView

from home.views import (
    DeviceViewSet,
    LightViewSet,
    SwitchViewSet,
    FanViewSet,
    WindowViewset,
    CurtainViewSet,
    SensorViewSet,
    PlanViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'lights', LightViewSet)
router.register(r'switchs', SwitchViewSet)
router.register(r'fans', FanViewSet)
router.register(r'windows', WindowViewset)
router.register(r'curtains', CurtainViewSet)
router.register(r'sensors', SensorViewSet)
router.register(r'plans', PlanViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('docs/', include_docs_urls(title='测试平台接口文档')),
]
