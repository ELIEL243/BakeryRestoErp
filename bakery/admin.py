from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Role)
admin.site.register(Agent)
admin.site.register(Unite)
admin.site.register(MatierePremiere)
admin.site.register(ProduitFini)
admin.site.register(Fourniture)
admin.site.register(Fournisseur)
admin.site.register(CommandeFourniture)
admin.site.register(CommandeMp)
admin.site.register(LigneCommandeMp)
admin.site.register(LigneCommandeFourniture)
admin.site.register(EntreeMp)
admin.site.register(EntreePF)
admin.site.register(EntreeFourniture)
admin.site.register(SortiePF)
admin.site.register(SortieMp)
admin.site.register(SortieFourniture)
admin.site.register(Paiement)
admin.site.register(PfHasPrice)
