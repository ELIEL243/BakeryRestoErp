# Generated by Django 5.0 on 2024-01-09 11:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0037_alter_commandefourniture_ref_alter_commandemp_ref_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commandefourniture',
            name='ref',
            field=models.CharField(default='2d7b1aff97', max_length=10),
        ),
        migrations.AlterField(
            model_name='commandemp',
            name='ref',
            field=models.CharField(default='e176edfb02', max_length=10, verbose_name='réference'),
        ),
        migrations.AlterField(
            model_name='invendupf',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 1, 9, 11, 18, 20, 454024), null=True),
        ),
        migrations.AlterField(
            model_name='invendupf',
            name='heure',
            field=models.TimeField(default=datetime.datetime(2024, 1, 9, 11, 18, 20, 454040), null=True),
        ),
    ]
