from django.conf.urls import url
from .views import resource_list

urls = [
    url(r'^$', resource_list),
]
