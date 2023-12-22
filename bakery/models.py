from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from auth_user.models import Role
import uuid
from django.utils import timezone
import datetime
# Create your models here.

devises = (
    ('USD', 'USD'),
    ('FC', 'FC'),
)


def generate_unique_uid():
    return uuid.uuid4().hex[:10]


class Taux(models.Model):
    valeur = models.DecimalField(max_digits=10, decimal_places=2)


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    initial = models.CharField(max_length=10, blank=True, default="")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        initial = self.name.split(' ')
        final_initial = ""
        for i in initial:
            final_initial += i[0]
        self.initial = final_initial
        super(Agent, self).save(*args, **kwargs)


class Unite(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MatierePremiere(models.Model):
    libelle = models.CharField(max_length=255)
    description = models.TextField()
    unite = models.ForeignKey(Unite, on_delete=models.CASCADE)
    critic_qts = models.IntegerField(default=0, blank=True, null=True)

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
            total -= out.qts
        return total


class ProduitFini(models.Model):
    libelle = models.CharField(max_length=255)
    description = models.TextField()
    unite = models.ForeignKey(Unite, on_delete=models.CASCADE)
    critic_qts = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.libelle

    @property
    def in_stock(self):
        total = 0
        entries = EntreePF.objects.filter(produit_fini=self)
        outs = SortiePF.objects.filter(produit_fini=self)
        for entry in entries:
            total += entry.qts
        for out in outs:
            total -= out.qts
        return total


class Fourniture(models.Model):
    libelle = models.CharField(max_length=255)
    description = models.TextField()
    unite = models.ForeignKey(Unite, on_delete=models.CASCADE)
    critic_qts = models.IntegerField(default=0, blank=True, null=True)

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
            total -= out.qts
        return total


class Fournisseur(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name


class CommandeMp(models.Model):
    ref = models.CharField(max_length=10, default=generate_unique_uid())
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    etat = models.BooleanField(default=False)
    devise = models.CharField(max_length=25, null=True, blank=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.fournisseur.name + " " + str(self.date)

    @property
    def get_total(self):
        lines = LigneCommandeMp.objects.filter(commande=self)
        total = 0
        for line in lines:
            total += line.total_price
        return total


class CommandeFourniture(models.Model):
    ref = models.CharField(max_length=10, default=generate_unique_uid())
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    etat = models.BooleanField(default=False)
    devise = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return self.fournisseur.name + " " + str(self.date)

    def get_total(self):
        lines = LigneCommandeFourniture.objects.filter(commande=self)
        total = 0
        for line in lines:
            total += line.total_price
        return total


class LigneCommandeMp(models.Model):
    commande = models.ForeignKey(CommandeMp, on_delete=models.CASCADE, null=True)
    matiere_premiere = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE, null=True)
    qts = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    devise = models.CharField(max_length=25, choices=devises, default=devises[1])

    def __str__(self):
        return self.matiere_premiere.libelle + " " + str(self.qts)

    @property
    def get_total(self):
        return str(self.total_price)


class LigneCommandeFourniture(models.Model):
    commande = models.ForeignKey(CommandeFourniture, on_delete=models.CASCADE, null=True)
    fourniture = models.ForeignKey(Fourniture, on_delete=models.CASCADE)
    qts = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    devise = models.CharField(max_length=25, choices=devises, default=devises[1])

    def __str__(self):
        return self.fourniture.libelle + " " + str(self.qts)

    @property
    def get_total(self):
        return str(self.total_price)


class EntreeMp(models.Model):
    matiere_premiere = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE, null=True)
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    date_exp = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    devise = models.CharField(max_length=25, choices=devises, default=devises[1])
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.matiere_premiere.libelle + " " + str(self.qts)

    @property
    def get_expiration_days(self):
        date_actuelle = datetime.date.today()
        days = 0
        if self.date_exp is not None:
            days = self.date_exp - date_actuelle
        return days.days


class EntreePF(models.Model):
    produit_fini = models.ForeignKey(ProduitFini, on_delete=models.CASCADE, null=True)
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.produit_fini.libelle + " " + str(self.qts)


class EntreeFourniture(models.Model):
    fourniture = models.ForeignKey(Fourniture, on_delete=models.CASCADE, null=True)
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    devise = models.CharField(max_length=25, choices=devises, default=devises[1])
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.fourniture.libelle + " " + str(self.qts)


class SortieMp(models.Model):
    matiere_premiere = models.ForeignKey(MatierePremiere, on_delete=models.CASCADE, null=True)
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.matiere_premiere.libelle + " " + str(self.qts)


class SortieFourniture(models.Model):
    fourniture = models.ForeignKey(Fourniture, on_delete=models.CASCADE)
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.fourniture.libelle + " " + str(self.qts)


class SortiePF(models.Model):
    produit_fini = models.ForeignKey(ProduitFini, on_delete=models.CASCADE, null=True)
    qts = models.IntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    devise = models.CharField(max_length=25, choices=devises, default=devises[1])
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.produit_fini.libelle + " " + str(self.qts)


class Paiement(models.Model):
    agent_rec = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True)
    agent_pai = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True, related_name='agent_pai')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True, null=True)
    devise = models.CharField(max_length=25, choices=devises, default=devises[1])
    heure = models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.agent_rec.name + " " + str(self.total)


class PfHasPrice(models.Model):
    produit_fini = models.ForeignKey(ProduitFini, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_updated = models.DateField(auto_now_add=True, null=True)
    devise = models.CharField(max_length=25, choices=devises, default=devises[1])
    heure_updated = models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.produit_fini.libelle + " " + str(self.price) + " " + str(self.date_updated)


# Signaux Pour les matieres premieres


@receiver(post_save, sender=User)
def create_agent(sender, instance, created, **kwargs):
    if created:
        Agent.objects.create(user=instance)