# Generated by Django 5.0 on 2024-01-08 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0030_entreemp_is_read_expired_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='taux',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='taux',
            name='heure',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='commandefourniture',
            name='ref',
            field=models.CharField(default='1cd549705c', max_length=10),
        ),
        migrations.AlterField(
            model_name='commandemp',
            name='ref',
            field=models.CharField(default='c936616215', max_length=10),
        ),
    ]
