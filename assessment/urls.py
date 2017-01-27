# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from ship.api import ShipViewSet


router = routers.DefaultRouter()
router.register(r'ships', ShipViewSet, base_name='ship')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(router.urls)),
]
