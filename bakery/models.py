import django.utils.timezone
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from auth_user.models import Role
import uuid
from django.utils import timezone
import datetime
from django.db.models import Q

# Create your models here.

devises = (
    ('USD', 'USD'),
    ('FC', 'FC'),
)

types_produit = (
    ('BOULANGERIE', 'BOULANGERIE'),
    ('RESTAURANT', 'RESTAURANT'),
    ('PACK', 'PACK'),
    ('BOULANGERIE ET RESTAURANT', 'BOULANGERIE ET RESTAURANT'),
    ('BOULANGERIE ET PACK', 'BOULANGERIE ET PACK'),
)


def generate_unique_uid():
    return uuid.uuid4().hex[:10]


class Taux(models.Model):
    class Meta:
        verbose_name = "Taux de change"

    valeur = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.valeur) + " " + str(self.date)


class Agent(models.Model):
    class Meta:
        verbose_name = "Agent"

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="nom")
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name="téléphone")
    initial = models.CharField(max_length=10, blank=True, default="")

    def __str__(self):
        if self.name is not None:
            return self.name
        return self.user.username

    def save(self, *args, **kwargs):
        if self.name is not None:
            initial = self.name.split(' ')
            final_initial = ""
            for i in initial:
                final_initial += i[0]
            self.initial = final_initial
        super(Agent, self).save(*args, **kwargs)


class Unite(models.Model):
    class Meta:
        verbose_name = "Unité de mésure"

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MatierePremiere(models.Model):
    class Meta:
        verbose_name = "Matière première"

    libelle = models.CharField(max_length=255)
    description = models.TextField()
    unite = models.ForeignKey(Unite, on_delete=models.CASCADE)
    critic_qts = models.IntegerField(default=0, blank=True, null=True)
    total_entry = models.IntegerField(default=0, blank=True, null=True)
    total_out = models.IntegerField(default=0, blank=True, null=True)
    type_mp = models.CharField(choices=types_produit, max_length=100, null=True, blank=True,
                               verbose_name="type de matière")

    def __str__(self):
        return self.libelle

    @property
    def in_stock(self):
        total = 0
        entries = EntreeMp.objects.filter(matiere_premiere=self)
        outs = SortieMp.objects.filter(matiere_premiere=self)
        for entry in entries:
            total += entry.qts
        for out in outs:
            if out.qts <= total:
                total -= out.qts
        return total

    @property
    def in_stock_pt(self):
        total = 0
        entries = EntreeMpPt.objects.filter(matiere_premiere=self)
        outs = SortieMpPt.objects.filter(matiere_premiere=self)
        for entry in entries:
            total += entry.qts
        for out in outs:
            if out.qts <= total:
                total -= out.qts
        return total

    @property
    def in_stock_pack(self):
        total = 0
        from foodpack.models import EntreeMpPack, SortieMpPack
        entries = EntreeMpPack.objects.filter(matiere_premiere=self)
        outs = SortieMpPack.objects.filter(matiere_premiere=self)
        for entry in entries:
            total += entry.qts
        for out in outs:
            if out.qts <= total:
                total -= out.qts
        return total

    @property
    def qts_out(self):
        total = 0
        outs = SortieMp.objects.filter(matiere_premiere=self, date=datetime.datetime.today().date())
        for out in outs:
            total += out.qts
        return total

    @property
    def qts_out_pt(self):
        total = 0
        outs = SortieMpPt.objects.filter(matiere_premiere=self, date=datetime.datetime.today().date())
        for out in outs:
            total += out.qts
        return total

    @property
    def qts_out_pack(self):
        total = 0
        from foodpack.models import SortieMpPack
        outs = SortieMpPack.objects.filter(matiere_premiere=self, date=datetime.datetime.today().date())
        for out in outs:
            total += out.qts
        return total

    @property
    def qts_enters(self):
        total = 0
        entries = EntreeMp.objects.filter(matiere_premiere=self, date=datetime.datetime.today().date())
        for entry in entries:
            total += entry.qts
        return total

    @property
    def qts_enters_pt(self):
        total = 0
        entries = EntreeMpPt.objects.filter(matiere_premiere=self, date=datetime.datetime.today().date())
        for entry in entries:
            total += entry.qts
        return total

    @property
    def qts_enters_pack(self):
        total = 0
        from foodpack.models import EntreeMpPack
        entries = EntreeMpPack.objects.filter(matiere_premiere=self, date=datetime.datetime.today().date())
        for entry in entries:
            total += entry.qts
        return total

    def qts_out_by_date(self, date1, date2):
        total = 0
        outs = None
        if date2 == "" or date2 is None:
            outs = SortieMp.objects.filter(matiere_premiere=self, date=date1)
        else:
            outs = SortieMp.objects.filter(matiere_premiere=self).filter(Q(date__gte=date1) & Q(date__lte=date2))
        for out in outs:
            total += out.qts
        return total

    def qts_out_by_date_pt(self, date1, date2):
        total = 0
        outs = None
        if date2 == "" or date2 is None:
            outs = SortieMpPt.objects.filter(matiere_premiere=self, date=date1)
        else:
            outs = SortieMpPt.objects.filter(matiere_premiere=self).filter(Q(date__gte=date1) & Q(date__lte=date2))
        for out in outs:
            total += out.qts
        return total

    def qts_enter_by_date(self, date1, date2):
        total = 0
        entries = None
        if date2 == "" or date2 is None:
            entries = EntreeMp.objects.filter(matiere_premiere=self, date=date1)
        else:
            entries = EntreeMp.objects.filter(matiere_premiere=self).filter(Q(date__gte=date1) & Q(date__lte=date2))
        for entry in entries:
            total += entry.qts
        return total

    def qts_enter_by_date_pt(self, date1, date2):
        total = 0
        entries = None
        if date2 == "" or date2 is None:
            entries = EntreeMpPt.objects.filter(matiere_premiere=self, date=date1)
        else:
            entries = EntreeMpPt.objects.filter(matiere_premiere=self).filter(Q(date__gte=date1) & Q(date__lte=date2))
        for entry in entries:
            total += entry.qts
        return total


class ProduitFini(models.Model):
    class Meta:
        verbose_name = "Produit fini"

    libelle = models.CharField(max_length=255)
    description = models.TextField()
    unite = models.ForeignKey(Unite, on_delete=models.CASCADE)
    critic_qts = models.IntegerField(default=0, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0, verbose_name="prix")
    type_produit = models.CharField(choices=types_produit, max_length=100, null=True, blank=True,
                                    verbose_name="type de produit")
    total_entry = models.IntegerField(default=0, blank=True, null=True)
    total_out = models.IntegerField(default=0, blank=True, null=True)
    total_sale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
        return self.libelle

    @property
    def get_price(self):
        return str(round(self.price, 0))

    @property
    def in_stock(self):
        total = 0
        entries = EntreePF.objects.filter(produit_fini=self)
        outs = SortiePF.objects.filter(produit_fini=self)
        for entry in entries:
            total += entry.qts
        for out in outs:
            if out.qts <= total:
                total -= out.qts
        return total

    @property
    def in_stock_pt(self):
        total = 0
        entries = EntreePfPt.objects.filter(produit_fini=self)
        outs = SortiePfPt.objects.filter(produit_fini=self)
        for entry in entries:
            total += entry.qts
        for out in outs:
            if out.qts <= total:
                total -= out.qts
        return total

    @property
    def qts_out(self):
        total = 0
        outs = SortiePF.objects.filter(produit_fini=self, date=datetime.datetime.today().date())
        for out in outs:
            total += out.qts
        return total

    @property
    def qts_out_pt(self):
        total = 0
        outs = SortiePfPt.objects.filter(produit_fini=self, date=datetime.datetime.today().date())
        for out in outs:
            total += out.qts
        return total

    @property
    def qts_enters(self):
        total = 0
        entries = EntreePF.objects.filter(produit_fini=self, date=datetime.datetime.today().date())
        for entry in entries:
            total += entry.qts
        return total

    @property
    def qts_enters_pt(self):
        total = 0
        entries = EntreePfPt.objects.filter(produit_fini=self, date=datetime.datetime.today().date())
        for entry in entries:
            total += entry.qts
        return total

    def qts_out_by_date(self, date1, date2):
        total = 0
        outs = None
        if date2 == "" or date2 is None:
            outs = SortiePF.objects.filter(produit_fini=self, date=date1)
        else:
            outs = SortiePF.objects.filter(produit_fini=self).filter(Q(date__gte=date1) & Q(date__lte=date2))
        for out in outs:
            total += out.qts
        return total

    def qts_out_by_date_pt(self, date1, date2):
        total = 0
        outs = None
        if date2 == "" or date2 is None:
            outs = SortiePfPt.objects.filter(produit_fini=self, date=date1)
        else:
            outs = SortiePfPt.objects.filter(produit_fini=self).filter(Q(date__gte=date1) & Q(date__lte=date2))
        for out in outs:
            total += out.qts
        return total

    def qts_enter_by_date(self, date1, date2):
        total = 0
        entries = None
        if date2 == "" or date2 is None:
            entries = EntreePF.objects.filter(produit_fini=self, date=date1)
        else:
            entries = EntreePF.objects.filter(produit_fini=self).filter(Q(date__gte=date1) & Q(date__lte=date2))
        for entry in entries:
            total += entry.qts
        return total

    def qts_enter_by_date_pt(self, date1, date2):
        total = 0
        entries = None
        if date2 == "" or date2 is None:
            entries = EntreePfPt.objects.filter(produit_fini=self, date=date1)
        else:
            entries = EntreePfPt.objects.filter(produit_fini=self).filter(Q(date__gte=date1) & Q(date__lte=date2))
        for entry in entries:
            total += entry.qts
        return total

    def total_sale_by_date(self, date1, date2):
        total_sale = 0
        outs = None
        invendus = None
        if date2 == "" or date2 is None:
            outs = SortiePF.objects.filter(produit_fini=self, date=date1)
            invendus = InvenduPf.objects.filter(produit_fini=self, date=date1)
            for o in outs:
                total_sale += o.total_cost
            for i in invendus:
                total_sale -= i.price
        else:
            outs = SortiePF.objects.filter(produit_fini=self).filter(Q(date__gte=date1) & Q(date__lte=date2))
            invendus = InvenduPf.objects.filter(produit_fini=self).filter(Q(date__gte=date1) & Q(date__lte=date2))
            for o in outs:
                total_sale += o.total_cost
            for i in invendus:
                total_sale -= i.price
        return total_sale

    def total_sale_by_date_pt(self, date1, date2):
        total_sale = 0
        outs = None
        if date2 == "" or date2 is None:
            outs = SortiePfPt.objects.filter(produit_fini=self, date=date1)
            for o in outs:
                total_sale += o.total_cost
        else:
            outs = SortiePfPt.objects.filter(produit_fini=self).filter(Q(date__gte=date1) & Q(date__lte=date2))
            for o in outs:
                total_sale += o.total_cost
        return total_sale


class Fourniture(models.Model):
    libelle = models.CharField(max_length=255)
    description = models.TextField()
    unite = models.ForeignKey(Unite, on_delete=models.CASCADE)
    critic_qts = models.IntegerField(default=0, blank=True, null=True)
    total_entry = models.IntegerField(default=0, blank=True, null=True)
    total_out = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.libelle

    @property
    def in_stock(self):
        total = 0
        entries = EntreeFourniture.objects.filter(fourniture=self)
        outs = SortieFourniture.objects.filter(fourniture=self)
        for entry in entries:
            total += entry.qts
        for out in outs:
            if out.qts <= total:
                total -= out.qts
        return total

    @property
    def qts_out(self):
        total = 0
        outs = SortieFourniture.objects.filter(fourniture=self, date=datetime.datetime.today().date())
        for out in outs:
            total += out.qts
        return total

    @property
    def qts_enters(self):
        total = 0
        entries = EntreeFourniture.objects.filter(fourniture=self, date=datetime.datetime.today().date())
        for entry in entries:
            total += entry.qts
        return total

    def qts_out_by_date(self, date1, date2):
        total = 0
        outs = None
        if date2 == "" or date2 is None:
            outs = SortieFourniture.objects.filter(fourniture=self, date=date1)
        else:
            outs = SortieFourniture.objects.filter(fourniture=self).filter(Q(date__gte=date1) & Q(date__lte=date2))
        for out in outs:
            total += out.qts
        return total

    def qts_enter_by_date(self, date1, date2):
        total = 0
        entries = None
        if date2 == "" or date2 is None:
            entries = EntreeFourniture.objects.filter(fourniture=self, date=date1)
        else:
            entries = EntreeFourniture.objects.filter(fourniture=self).filter(Q(date__gte=date1) & Q(date__lte=date2))
        for entry in entries:
            total += entry.qts
        return total


class Fournisseur(models.Model):
    name = models.CharField(max_length=255, verbose_name="nom")
    phone = models.CharField(max_length=15, verbose_name="téléphone")
    email = models.EmailField()
    address = models.TextField(verbose_name="adresse")

    def __str__(self):
        return self.name


class CommandeMp(models.Model):
    class Meta:
        verbose_name = "Commande de matière première"

    ref = models.CharField(max_length=10, default=generate_unique_uid(), verbose_name="réference")
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True, null=True, verbose_name="date de commande")
    heure = models.TimeField(auto_now_add=True, null=True)
    etat = models.BooleanField(default=False)
    devise = models.CharField(max_length=25, null=True, blank=True)
    delivered_at = models.DateField(null=True, blank=True, verbose_name="date de livraison")

    @property
    def get_total(self):
        lines = LigneCommandeMp.objects.filter(commande=self)
        total = 0
        for line in lines:
            total += line.total_price
        return total


class CommandeFourniture(models.Model):
    class Meta:
        verbose_name = "Commande de fourniture"

    ref = models.CharField(max_length=10, default=generate_unique_uid())
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True, verbose_name="date de commande")
    heure = models.TimeField(auto_now_add=True, null=True)
    etat = models.BooleanField(default=False)
    devise = models.CharField(max_length=25, null=True, blank=True)
    delivered_at = models.DateField(null=True, blank=True, verbose_name="date de livraison")

    @property
    def get_total(self):
        lines = LigneCommandeFourniture.objects.filter(commande=self)
        total = 0
        for line in lines:
            total += line.total_price
        return total


class CommandePf(models.Model):
    class Meta:
        ordering = ["date"]
        verbose_name = "Ventes de produit finis"

    ref = models.CharField(max_length=10, default=generate_unique_uid(), verbose_name="réference")
    date = models.DateField(auto_now_add=True, null=True, verbose_name="date de commande")
    heure = models.TimeField(auto_now_add=True, null=True)
    etat = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    devise = models.CharField(max_length=25, null=True, blank=True)
    client = models.CharField(max_length=255, null=True, blank=True)
    table_number = models.IntegerField(default=1)
    date_time = models.DateTimeField(auto_now_add=True, null=True)
    cloture = models.BooleanField(default=False)

    @property
    def get_total(self):
        lines = LigneCommandePf.objects.filter(commande=self)
        total = 0
        for line in lines:
            total += line.get_total
        return total

    @property
    def get_subtotal(self):
        return self.get_total - (self.get_total * 16) / 100

    @property
    def get_total_tax(self):
        return (self.get_total * 16) / 100


class LigneCommandeMp(models.Model):
    commande = models.ForeignKey(CommandeMp, on_delete=models.CASCADE, null=True)
    matiere_premiere = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE, null=True)
    qts = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    devise = models.CharField(max_length=25, choices=devises, default=devises[1][0])
    taux = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
        return self.matiere_premiere.libelle + " " + str(self.qts)

    @property
    def get_total(self):
        return str(round(self.total_price, 0))


class LigneCommandeFourniture(models.Model):
    commande = models.ForeignKey(CommandeFourniture, on_delete=models.CASCADE, null=True)
    fourniture = models.ForeignKey(Fourniture, on_delete=models.CASCADE)
    qts = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    devise = models.CharField(max_length=25, choices=devises, default=devises[1][0])
    taux = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
        return self.fourniture.libelle + " " + str(self.qts)

    @property
    def get_total(self):
        return str(self.total_price)


class LigneCommandePf(models.Model):
    commande = models.ForeignKey(CommandePf, on_delete=models.CASCADE, null=True)
    produit_fini = models.ForeignKey(ProduitFini, on_delete=models.CASCADE)
    qts = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    devise = models.CharField(max_length=25, choices=devises, default=devises[1][0])
    taux = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
        return self.produit_fini.libelle + " " + str(self.qts)

    @property
    def get_total(self):
        return self.qts * self.price


class EntreeMp(models.Model):
    class Meta:
        verbose_name = "Entrées de matière première"

    matiere_premiere = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE, null=True,
                                         verbose_name="matière première")
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    date_exp = models.DateField(null=True, blank=True, verbose_name="date expiration")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="cout total")
    devise = models.CharField(max_length=25, choices=devises, default=devises[1][0])
    completed = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True, null=True)
    is_read_expired = models.BooleanField(default=False)
    taux = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
        return self.matiere_premiere.libelle + " " + str(self.qts)

    @property
    def get_expiration_days(self):
        date_actuelle = datetime.date.today()
        days = 0
        if self.date_exp is not None:
            days = self.date_exp - date_actuelle
        return days.days

    @property
    def in_stock(self):
        total = 0
        entries = EntreeMp.objects.filter(added_at__lt=self.added_at, matiere_premiere=self.matiere_premiere)
        outs = SortieMp.objects.filter(added_at__lt=self.added_at, matiere_premiere=self.matiere_premiere)
        for entry in entries:
            total += entry.qts
        for o in outs:
            if o.qts <= total:
                total -= o.qts
        return total + self.qts


class EntreeMpPt(models.Model):
    class Meta:
        verbose_name = "Entrées de matière première"

    matiere_premiere = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE, null=True,
                                         verbose_name="matière première")
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    date_exp = models.DateField(null=True, blank=True, verbose_name="date expiration")
    completed = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True, null=True)
    is_read_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.matiere_premiere.libelle + " " + str(self.qts)

    @property
    def get_expiration_days(self):
        date_actuelle = datetime.date.today()
        days = 0
        if self.date_exp is not None:
            days = self.date_exp - date_actuelle
        return days.days

    @property
    def in_stock(self):
        total = 0
        entries = EntreeMpPt.objects.filter(added_at__lt=self.added_at, matiere_premiere=self.matiere_premiere)
        outs = SortieMpPt.objects.filter(added_at__lt=self.added_at, matiere_premiere=self.matiere_premiere)
        for entry in entries:
            total += entry.qts
        for o in outs:
            if o.qts <= total:
                total -= o.qts
        return total + self.qts


class EntreePF(models.Model):
    class Meta:
        verbose_name = "Entrées de produit fini"

    produit_fini = models.ForeignKey(ProduitFini, on_delete=models.CASCADE, null=True, verbose_name="produit fini")
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    completed = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.produit_fini.libelle + " " + str(self.qts)

    @property
    def in_stock(self):
        total = 0
        entries = EntreePF.objects.filter(added_at__lt=self.added_at, produit_fini=self.produit_fini)
        outs = SortiePF.objects.filter(added_at__lt=self.added_at, produit_fini=self.produit_fini)
        for entry in entries:
            total += entry.qts
        for o in outs:
            if o.qts <= total:
                total -= o.qts
        return total + self.qts


class EntreeFourniture(models.Model):
    class Meta:
        verbose_name = "Entrées de fourniture"

    fourniture = models.ForeignKey(Fourniture, on_delete=models.CASCADE, null=True)
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="cout total")
    devise = models.CharField(max_length=25, choices=devises, default=devises[1][0])
    completed = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True, null=True)
    taux = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
        return self.fourniture.libelle + " " + str(self.qts)

    @property
    def in_stock(self):
        total = 0
        entries = EntreeFourniture.objects.filter(added_at__lt=self.added_at, fourniture=self.fourniture)
        outs = SortieFourniture.objects.filter(added_at__lt=self.added_at, fourniture=self.fourniture)
        for entry in entries:
            total += entry.qts
        for o in outs:
            if o.qts <= total:
                total -= o.qts
        return total + self.qts


class EntreePfPt(models.Model):
    class Meta:
        verbose_name = "Entrées de produit fini du petit stock"

    produit_fini = models.ForeignKey(ProduitFini, on_delete=models.CASCADE, null=True, verbose_name="produit fini")
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    completed = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.produit_fini.libelle + " " + str(self.qts)

    @property
    def in_stock(self):
        total = 0
        entries = EntreePfPt.objects.filter(added_at__lt=self.added_at, produit_fini=self.produit_fini)
        outs = SortiePfPt.objects.filter(added_at__lt=self.added_at, produit_fini=self.produit_fini)
        for entry in entries:
            total += entry.qts
        for o in outs:
            if o.qts <= total:
                total -= o.qts
        return total + self.qts


class SortieMp(models.Model):
    class Meta:
        verbose_name = "Sortie de matière première"

    matiere_premiere = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE, null=True)
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    completed = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True, null=True)
    destination = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.matiere_premiere.libelle + " " + str(self.qts)

    @property
    def in_stock(self):
        total = 0
        entries = EntreeMp.objects.filter(added_at__lt=self.added_at, matiere_premiere=self.matiere_premiere)
        outs = SortieMp.objects.filter(added_at__lt=self.added_at, matiere_premiere=self.matiere_premiere)
        for entry in entries:
            total += entry.qts
        for o in outs:
            if o.qts <= total:
                total -= o.qts
        return total - self.qts


class SortieMpPt(models.Model):
    class Meta:
        verbose_name = "Sortie de matière première du petit stock"

    matiere_premiere = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE, null=True)
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    completed = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.matiere_premiere.libelle + " " + str(self.qts)

    @property
    def in_stock(self):
        total = 0
        entries = EntreeMpPt.objects.filter(added_at__lt=self.added_at, matiere_premiere=self.matiere_premiere)
        outs = SortieMpPt.objects.filter(added_at__lt=self.added_at, matiere_premiere=self.matiere_premiere)
        for entry in entries:
            total += entry.qts
        for o in outs:
            if o.qts <= total:
                total -= o.qts
        return total - self.qts


class SortieFourniture(models.Model):
    class Meta:
        verbose_name = "Sortie de fourniture"

    fourniture = models.ForeignKey(Fourniture, on_delete=models.CASCADE)
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    completed = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.fourniture.libelle + " " + str(self.qts)

    @property
    def in_stock(self):
        total = 0
        entries = EntreeFourniture.objects.filter(added_at__lt=self.added_at, fourniture=self.fourniture)
        outs = SortieFourniture.objects.filter(added_at__lt=self.added_at, fourniture=self.fourniture)
        for entry in entries:
            total += entry.qts
        for o in outs:
            if o.qts <= total:
                total -= o.qts
        return total - self.qts


class SortiePF(models.Model):
    class Meta:
        verbose_name = "Sortie de produit fini"

    produit_fini = models.ForeignKey(ProduitFini, on_delete=models.CASCADE, null=True)
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="prix")
    devise = models.CharField(max_length=25, choices=devises, default=devises[1][0])
    completed = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True, null=True)
    destination = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.produit_fini.libelle + " " + str(self.qts)

    @property
    def in_stock(self):
        total = 0
        entries = EntreePF.objects.filter(added_at__lt=self.added_at, produit_fini=self.produit_fini)
        outs = SortiePF.objects.filter(added_at__lt=self.added_at, produit_fini=self.produit_fini)
        for entry in entries:
            total += entry.qts
        for o in outs:
            if o.qts <= total:
                total -= o.qts
        return total - self.qts

    @property
    def total_cost(self):
        total = self.qts * self.price
        return total


class SortiePfPt(models.Model):
    class Meta:
        verbose_name = "Sortie de produit fini du petit stock"

    produit_fini = models.ForeignKey(ProduitFini, on_delete=models.CASCADE, null=True)
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="prix")
    devise = models.CharField(max_length=25, choices=devises, default=devises[1][0])
    completed = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.produit_fini.libelle + " " + str(self.qts)

    @property
    def in_stock(self):
        total = 0
        entries = EntreePfPt.objects.filter(added_at__lt=self.added_at, produit_fini=self.produit_fini)
        outs = SortiePfPt.objects.filter(added_at__lt=self.added_at, produit_fini=self.produit_fini)
        for entry in entries:
            total += entry.qts
        for o in outs:
            if o.qts <= total:
                total -= o.qts
        return total - self.qts

    @property
    def total_cost(self):
        total = self.qts * self.price
        return total


class InvenduPf(models.Model):
    class Meta:
        verbose_name = "Invendus de produit fini"

    produit_fini = models.ForeignKey(ProduitFini, on_delete=models.CASCADE, null=True, verbose_name="Produit fini")
    qts = models.IntegerField(null=True, blank=True, default=0)
    date = models.DateField(null=True, editable=True)
    heure = models.TimeField(null=True, editable=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="cout total")
    devise = models.CharField(max_length=25, choices=devises, default=devises[1][0])

    def __str__(self):
        return self.produit_fini.libelle + " " + str(self.qts)


class ChiffreAffaire(models.Model):
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    devise = models.CharField(max_length=25, choices=devises, default=devises[1][0])
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.date) + " " + str(self.total_price)


class Paiement(models.Model):
    agent_rec = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True)
    agent_pai = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True, related_name='agent_pai')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True, null=True)
    devise = models.CharField(max_length=25, choices=devises, default=devises[1][0])
    heure = models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.agent_rec.name + " " + str(self.total)


class PfHasPrice(models.Model):
    produit_fini = models.ForeignKey(ProduitFini, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_updated = models.DateField(auto_now_add=True, null=True)
    devise = models.CharField(max_length=25, choices=devises, default=devises[1][0])
    heure_updated = models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.produit_fini.libelle + " " + str(self.price) + " " + str(self.date_updated)


# Signaux Pour les matieres premieres


@receiver(post_save, sender=User)
def create_agent(sender, instance, created, **kwargs):
    if created:
        Agent.objects.create(user=instance)


@receiver(post_save, sender=SortiePF)
def create_sortie_pf_gr(sender, instance, created, **kwargs):
    if created:
        if instance.produit_fini.type_produit in ['BOULANGERIE ET RESTAURANT', 'RESTAURANT']:
            EntreePfPt.objects.create(produit_fini=instance.produit_fini, qts=instance.qts, completed=True)
        else:
            pass


@receiver(post_save, sender=SortieMp)
def create_sortie_mp_gr(sender, instance, created, **kwargs):
    if created:
        if instance.destination == "PETIT STOCK":
            EntreeMpPt.objects.create(matiere_premiere=instance.matiere_premiere, qts=instance.qts, completed=True)
        elif instance.destination == "FOOD PACK":
            from foodpack.models import EntreeMpPack
            EntreeMpPack.objects.create(matiere_premiere=instance.matiere_premiere, qts=instance.qts, completed=True)
