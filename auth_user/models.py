from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserHasRole(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
