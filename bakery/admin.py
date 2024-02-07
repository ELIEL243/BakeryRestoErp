from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class LineItemMpAdmin(admin.TabularInline):
    model = LigneCommandeMp
    exclude = ('taux', )


class LineItemFournitureAdmin(admin.TabularInline):
    model = LigneCommandeFourniture
    exclude = ('taux', )


class AgentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'email', 'phone',)
    search_fields = ('name', 'email', 'phone',)


class UnitAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class TauxAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('valeur', 'date', 'heure',)
    search_fields = ('date', )


class MatierePremierAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('libelle', 'description', 'unite', 'critic_qts', 'in_stock')
    search_fields = ('libelle', 'description', 'unite', )


class ProduitFiniAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('libelle', 'description', 'unite', 'price', 'critic_qts', 'in_stock', )
    search_fields = ('libelle', 'description', 'unite', )


class FournitureAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('libelle', 'description', 'unite', 'critic_qts', 'in_stock', )
    search_fields = ('libelle', 'description')


class FournisseurAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'address',)
    search_fields = ('name', 'phone', 'email',)


class CommandeMpAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('ref', 'fournisseur', 'date', 'heure', 'etat', 'delivered_at', 'get_total', 'devise')
    search_fields = ('ref', 'fournisseur', 'date', 'heure', 'etat', )
    list_filter = ('ref', 'fournisseur', 'date', 'heure', 'etat', )
    inlines = [LineItemMpAdmin, ]


class CommandeFournitureAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('ref', 'fournisseur', 'date', 'heure', 'etat', 'delivered_at', 'get_total', 'devise')
    search_fields = ('ref', 'fournisseur', 'date', 'heure', 'etat',)
    list_filter = ('ref', 'fournisseur', 'date', 'heure', 'etat',)
    inlines = [LineItemFournitureAdmin, ]


class EntreeMpAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('matiere_premiere', 'qts', 'date', 'heure', 'date_exp', 'price', 'devise')
    list_filter = ('matiere_premiere', 'date')
    search_fields = ('matiere_premiere', 'date')


class EntreeFournitureAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('fourniture', 'qts', 'date', 'heure', 'price', 'devise')
    list_filter = ('fourniture', 'date')
    search_fields = ('fourniture', 'date')


class EntrePfAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('produit_fini', 'qts', 'date', 'heure',)
    list_filter = ('produit_fini', 'date')
    search_fields = ('produit_fini', 'date')


class SortieMpAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('matiere_premiere', 'qts', 'date', 'heure',)
    search_fields = ('matiere_premiere', 'date',)
    list_filter = ('matiere_premiere', 'date',)


class SortieFournitureAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('fourniture', 'qts', 'date', 'heure',)
    search_fields = ('fourniture', 'date',)
    list_filter = ('fourniture', 'date',)


class SortiePfAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('produit_fini', 'qts', 'date', 'heure', 'price', 'devise',)
    search_fields = ('produit_fini', 'date',)
    list_filter = ('produit_fini', 'date',)


class InvenduAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('produit_fini', 'qts', 'date', 'heure', 'price', 'devise',)
    search_fields = ('produit_fini', 'date',)
    list_filter = ('produit_fini', 'date',)


class RoleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Role, RoleAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(Unite, UnitAdmin)
admin.site.register(MatierePremiere, MatierePremierAdmin)
admin.site.register(ProduitFini, ProduitFiniAdmin)
admin.site.register(Fourniture, FournitureAdmin)
admin.site.register(Fournisseur, FournisseurAdmin)
admin.site.register(CommandeFourniture, CommandeFournitureAdmin)
admin.site.register(CommandeMp, CommandeMpAdmin)
admin.site.register(EntreeMp, EntreeMpAdmin)
admin.site.register(EntreeMpPt)
admin.site.register(EntreePfPt)
admin.site.register(EntreePF, EntrePfAdmin)
admin.site.register(EntreeFourniture, EntreeFournitureAdmin)
admin.site.register(SortiePF, SortiePfAdmin)
admin.site.register(SortieMp, SortieMpAdmin)
admin.site.register(SortieFourniture, SortieFournitureAdmin)
admin.site.register(Taux, TauxAdmin)
admin.site.register(InvenduPf, InvenduAdmin)
admin.site.register(ChiffreAffaire)

admin.site.site_title = _("BOULANGERIE ICLASS")
admin.site.site_header = _("BOULANGERIE ICLASS")
admin.site.index_title = _("BOULANGERIE ICLASS")
