from django.contrib import admin
from configurator.apps.resource.admin import ResourceChildAdmin
from .models import *

admin.site.register(PostgreSQLServer)

@admin.register(PostgreSQLDatabaseAccess)
class PostgreSQLDatabaseAccessAdmin(ResourceChildAdmin):
    base_model = PostgreSQLDatabaseAccess
    show_in_index = True
