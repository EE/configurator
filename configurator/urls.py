"""configurator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
import configurator.apps.http_resource.urls as http_res
import configurator.apps.application.urls as app
import configurator.apps.resource.urls as resource

API_PREFIX = 'api/'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^{}app/'.format(API_PREFIX), include(app.urls)),
    url(r'^{}httpres/'.format(API_PREFIX), include(http_res.urls)),
    url(r'^{}resource/'.format(API_PREFIX), include(resource.urls)),
    url(r'^api-rest/', include('rest_framework.urls', namespace='rest_framework'))
]
