import datetime
from django.db import models

from bakery.models import MatierePremiere

# Create your models here.


devises = (
    ('USD', 'USD'),
    ('FC', 'FC'),
)


class Entreprise(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    mail = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=14, null=True, blank=True)

    def __str__(self):
        return self.name


class FoodPack(models.Model):
    class Meta:
        verbose_name = "Pack"
    libelle = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0, verbose_name="prix")
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
        entries = EntreePack.objects.filter(pack=self)
        outs = SortiePack.objects.filter(pack=self)
        for entry in entries:
            total += entry.qts
        for out in outs:
            total -= out.qts
        return total

    @property
    def qts_out(self):
        total = 0
        outs = SortiePack.objects.filter(pack=self, date=datetime.datetime.today().date())
        for out in outs:
            total += out.qts
        return total

    @property
    def qts_enters(self):
        total = 0
        entries = EntreePack.objects.filter(pack=self, date=datetime.datetime.today().date())
        for entry in entries:
            total += entry.qts
        return total


class EntreePack(models.Model):
    class Meta:
        verbose_name = "Entrées des packs"
    pack = models.ForeignKey(FoodPack, on_delete=models.CASCADE, null=True, verbose_name="pack")
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    completed = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.pack.libelle + " " + str(self.qts)

    @property
    def in_stock(self):
        total = 0
        entries = EntreePack.objects.filter(added_at__lt=self.added_at, pack=self.pack)
        outs = SortiePack.objects.filter(added_at__lt=self.added_at, pack=self.pack)
        for entry in entries:
            total += entry.qts
        for o in outs:
            total -= o.qts
        return total + self.qts


class SortiePack(models.Model):
    class Meta:
        verbose_name = "Livraisons des packs"
    pack = models.ForeignKey(FoodPack, on_delete=models.CASCADE, null=True)
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="prix")
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    devise = models.CharField(max_length=25, choices=devises, default=devises[1][0])
    completed = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.pack.libelle + " " + str(self.qts)

    @property
    def in_stock(self):
        total = 0
        entries = EntreePack.objects.filter(added_at__lt=self.added_at, pack=self.pack)
        outs = SortiePack.objects.filter(added_at__lt=self.added_at, pack=self.pack)
        for entry in entries:
            total += entry.qts
        for o in outs:
            total -= o.qts
        return total - self.qts

    @property
    def total_cost(self):
        total = self.qts * self.price
        return total


class InvenduPack(models.Model):
    class Meta:
        verbose_name = "Invendus de packs"
    pack = models.ForeignKey(FoodPack, on_delete=models.CASCADE, null=True)
    qts = models.IntegerField(null=True, blank=True, default=0)
    date = models.DateField(null=True, editable=True)
    heure = models.TimeField(null=True, editable=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="cout total")
    devise = models.CharField(max_length=25, choices=devises, default=devises[1][0])

    def __str__(self):
        return self.pack.libelle + " " + str(self.qts)


class SortieMpPack(models.Model):
    class Meta:
        verbose_name = "Sortie de matière première au service pack"

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
        entries = EntreeMpPack.objects.filter(added_at__lt=self.added_at, matiere_premiere=self.matiere_premiere)
        outs = SortieMpPack.objects.filter(added_at__lt=self.added_at, matiere_premiere=self.matiere_premiere)
        for entry in entries:
            total += entry.qts
        for o in outs:
            total -= o.qts
        return total - self.qts


class EntreeMpPack(models.Model):
    class Meta:
        verbose_name = "Entrées de matière première."

    matiere_premiere = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE, null=True,
                                         verbose_name="matière première")
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
        entries = EntreeMpPack.objects.filter(added_at__lt=self.added_at, matiere_premiere=self.matiere_premiere)
        outs = SortieMpPack.objects.filter(added_at__lt=self.added_at, matiere_premiere=self.matiere_premiere)
        for entry in entries:
            total += entry.qts
        for o in outs:
            total -= o.qts
        return total + self.qts
