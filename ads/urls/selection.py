from rest_framework import routers

from ads.views.ads import *
from ads.views.selection import SelectionViewSet

router = routers.SimpleRouter()
router.register('', SelectionViewSet)
urlpatterns = router.urls