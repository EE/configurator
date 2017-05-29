from django.contrib import admin
from .models import *
from polymorphic.admin import PolymorphicChildModelAdmin


class ResourceChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Resource


@admin.register(StringResource)
class StringResourceAdmin(ResourceChildAdmin):
    base_model = StringResource
    show_in_index = True


@admin.register(IntResource)
class IntResourceAdmin(ResourceChildAdmin):
    base_model = IntResource
    show_in_index = True


@admin.register(ListResource)
class ListResourceAdmin(ResourceChildAdmin):
    base_model = ListResource
    show_in_index = True


class DictResourceEntryInline(admin.TabularInline):
    model = DictResourceEntry
    fk_name = 'dictionary'


@admin.register(DictResource)
class DictResourceAdmin(ResourceChildAdmin):
    base_model = DictResource
    show_in_index = True
    inlines = [DictResourceEntryInline]
