from django.contrib import admin
from .models import *
from configurator.apps.resource.admin import ResourceChildAdmin


class MountedFileInline(admin.TabularInline):
    model = MountedFile


@admin.register(AppResource)
class AppResourceAdmin(ResourceChildAdmin):
    base_model = AppResource
    show_in_index = True
    inlines = [MountedFileInline]
