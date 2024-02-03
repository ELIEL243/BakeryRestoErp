from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class UserHasRoleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['user', 'role']


admin.site.register(UserHasRole, UserHasRoleAdmin)
admin.site.register(AffectedRoles, UserHasRoleAdmin)
