from django.contrib import admin
from .models import *
from configurator.apps.resource.admin import ResourceChildAdmin


@admin.register(HTTPResource)
class HTTPResourceAdmin(ResourceChildAdmin):
    base_model = HTTPResource
    show_in_index = True
