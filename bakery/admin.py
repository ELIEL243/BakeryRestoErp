from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
# Register your models here.


class LineItemMpAdmin(admin.TabularInline):
    model = LigneCommandeMp
    exclude = ('taux', )


class LineItemFournitureAdmin(admin.TabularInline):
    model = LigneCommandeFourniture
    exclude = ('taux', )


class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone',)
    search_fields = ('name', 'email', 'phone',)


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class TauxAdmin(admin.ModelAdmin):
    list_display = ('valeur', 'date', 'heure',)
    search_fields = ('date', )


class MatierePremierAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'description', 'unite', 'critic_qts', 'in_stock')
    search_fields = ('libelle', 'description', 'unite', )


class ProduitFiniAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'description', 'unite', 'price', 'critic_qts', 'in_stock', )
    search_fields = ('libelle', 'description', 'unite', )


class FournitureAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'description', 'unite', 'critic_qts', 'in_stock', )
    search_fields = ('libelle', 'description')


class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'address',)
    search_fields = ('name', 'phone', 'email',)


class CommandeMpAdmin(admin.ModelAdmin):
    list_display = ('ref', 'fournisseur', 'date', 'heure', 'etat', 'delivered_at', 'get_total', 'devise')
    search_fields = ('ref', 'fournisseur', 'date', 'heure', 'etat', )
    list_filter = ('ref', 'fournisseur', 'date', 'heure', 'etat', )
    inlines = [LineItemMpAdmin, ]


class CommandeFournitureAdmin(admin.ModelAdmin):
    list_display = ('ref', 'fournisseur', 'date', 'heure', 'etat', 'delivered_at', 'get_total', 'devise')
    search_fields = ('ref', 'fournisseur', 'date', 'heure', 'etat',)
    list_filter = ('ref', 'fournisseur', 'date', 'heure', 'etat',)
    inlines = [LineItemFournitureAdmin, ]


class EntreeMpAdmin(admin.ModelAdmin):
    list_display = ('matiere_premiere', 'qts', 'date', 'heure', 'date_exp', 'price', 'devise')
    list_filter = ('matiere_premiere', 'date')
    search_fields = ('matiere_premiere', 'date')


class EntreeFournitureAdmin(admin.ModelAdmin):
    list_display = ('fourniture', 'qts', 'date', 'heure', 'price', 'devise')
    list_filter = ('fourniture', 'date')
    search_fields = ('fourniture', 'date')


class EntrePfAdmin(admin.ModelAdmin):
    list_display = ('produit_fini', 'qts', 'date', 'heure',)
    list_filter = ('produit_fini', 'date')
    search_fields = ('produit_fini', 'date')


class SortieMpAdmin(admin.ModelAdmin):
    list_display = ('matiere_premiere', 'qts', 'date', 'heure',)
    search_fields = ('matiere_premiere', 'date',)
    list_filter = ('matiere_premiere', 'date',)


class SortieFournitureAdmin(admin.ModelAdmin):
    list_display = ('fourniture', 'qts', 'date', 'heure',)
    search_fields = ('fourniture', 'date',)
    list_filter = ('fourniture', 'date',)


class SortiePfAdmin(admin.ModelAdmin):
    list_display = ('produit_fini', 'qts', 'date', 'heure', 'price', 'devise',)
    search_fields = ('produit_fini', 'date',)
    list_filter = ('produit_fini', 'date',)


class InvenduAdmin(admin.ModelAdmin):
    list_display = ('produit_fini', 'qts', 'date', 'heure', 'price', 'devise',)
    search_fields = ('produit_fini', 'date',)
    list_filter = ('produit_fini', 'date',)


admin.site.register(Role)
admin.site.register(Agent, AgentAdmin)
admin.site.register(Unite, UnitAdmin)
admin.site.register(MatierePremiere, MatierePremierAdmin)
admin.site.register(ProduitFini, ProduitFiniAdmin)
admin.site.register(Fourniture, FournitureAdmin)
admin.site.register(Fournisseur, FournisseurAdmin)
admin.site.register(CommandeFourniture, CommandeFournitureAdmin)
admin.site.register(CommandeMp, CommandeMpAdmin)
admin.site.register(EntreeMp, EntreeMpAdmin)
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
