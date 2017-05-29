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


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/app/', include(app.urls)),
    url(r'^api/httpres/', include(http_res.urls)),
    url(r'^api/resource/', include(resource.urls)),
    url(r'^api-rest/', include('rest_framework.urls', namespace='rest_framework'))
]
