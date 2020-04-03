# -*- coding: utf-8 -*-

from django.urls import path
from rest_framework import routers
from . import views
from django.conf.urls import url, include

router = routers.DefaultRouter()

router.register(r'enterprise', views.EnterpriseViewSet)
router.register(r'person', views.PersonViewSet)
router.register(r'contract', views.ContractViewSet)

# urlpatterns = [
#    path(r'api/v1/', include(router.urls)),
# ]
urlpatterns = router.urls