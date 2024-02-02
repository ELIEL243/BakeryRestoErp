from django.contrib import admin
from bakery.models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class LineItemPfAdmin(admin.TabularInline):
    model = LigneCommandePf


class CommandePfAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('ref', 'client', 'date', 'heure', 'etat', 'cloture', 'get_total', 'devise')
    search_fields = ('ref', 'client', 'date', 'heure', 'etat', )
    list_filter = ('ref', 'client', 'date', 'heure', 'etat', )
    inlines = [LineItemPfAdmin, ]


admin.site.register(CommandePf, CommandePfAdmin)
