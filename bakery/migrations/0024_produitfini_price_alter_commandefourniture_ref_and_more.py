# Generated by Django 5.0 on 2023-12-29 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0023_entreefourniture_added_at_entreemp_added_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='produitfini',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='commandefourniture',
            name='ref',
            field=models.CharField(default='753ca8a25e', max_length=10),
        ),
        migrations.AlterField(
            model_name='commandemp',
            name='ref',
            field=models.CharField(default='f62294a339', max_length=10),
        ),
    ]
