from django.contrib import admin
from django.urls import path
from rest_framework import routers

from ads.views.ads import *

router = routers.SimpleRouter()
router.register('', AdViewSet)
urlpatterns = router.urls


