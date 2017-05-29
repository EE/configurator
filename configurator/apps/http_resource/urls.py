from rest_framework import routers
from configurator.apps.http_resource import views as httpviews

router = routers.DefaultRouter()
router.register(r'^$', httpviews.HTTPResourceViewSet)

urls = router.urls
