# Generated by Django 5.0 on 2024-02-01 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0002_remove_userhasrole_name_userhasrole_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userhasrole',
            options={'verbose_name': 'Roles utilisateur'},
        ),
    ]
