from configurator.apps.resource.views import ResourceDetail, ResourceList
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', ResourceList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', ResourceDetail.as_view()),
]

urls = format_suffix_patterns(urlpatterns)
