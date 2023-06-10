from django.contrib import admin
from django.urls import path
from rest_framework import routers

from ads.views.category import *

router = routers.SimpleRouter()
router.register('', CategoryViewSet)
urlpatterns = router.urls