# Generated by Django 5.0 on 2024-01-08 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0031_taux_date_taux_heure_alter_commandefourniture_ref_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='entreefourniture',
            name='taux',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='entreemp',
            name='taux',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='lignecommandefourniture',
            name='taux',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='lignecommandemp',
            name='taux',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='commandefourniture',
            name='ref',
            field=models.CharField(default='2468b8c485', max_length=10),
        ),
        migrations.AlterField(
            model_name='commandemp',
            name='ref',
            field=models.CharField(default='50928ec17c', max_length=10),
        ),
    ]
