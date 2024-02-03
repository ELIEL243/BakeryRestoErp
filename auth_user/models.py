from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserHasRole(models.Model):
    class Meta:
        verbose_name = "Roles utilisateur"
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " - " + self.role.name


class AffectedRoles(models.Model):
    class Meta:
        verbose_name = "Roles utilisateur2"
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " - " + self.role.name

@receiver(post_save, sender=UserHasRole)
def create_role_agent(sender, instance, created, **kwargs):
    if created:
        if instance.role.name == "grand stock et boulangerie":
            user = instance.user
            user.is_superuser = True
            user.save()
