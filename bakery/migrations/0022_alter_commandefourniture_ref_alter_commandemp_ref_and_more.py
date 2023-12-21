# Generated by Django 5.0 on 2023-12-21 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0021_alter_commandefourniture_ref_alter_commandemp_ref_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commandefourniture',
            name='ref',
            field=models.CharField(default='38b2f5ea08', max_length=10),
        ),
        migrations.AlterField(
            model_name='commandemp',
            name='ref',
            field=models.CharField(default='93ebab5a54', max_length=10),
        ),
        migrations.AlterField(
            model_name='lignecommandefourniture',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='lignecommandemp',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]
