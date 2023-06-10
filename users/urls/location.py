from django.contrib import admin
from rest_framework import routers

from users.views.location import *

router = routers.SimpleRouter()
router.register('', LocationViewSet)
urlpatterns = router.urls

