from rest_framework import routers
from configurator.apps.application import views as appviews

router = routers.DefaultRouter()
router.register(r'^$', appviews.AppViewSet)

urls = router.urls
