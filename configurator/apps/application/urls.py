
from configurator.apps.application.views import AppDetail, AppList
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', AppList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', AppDetail.as_view()),
]

urls = format_suffix_patterns(urlpatterns)
