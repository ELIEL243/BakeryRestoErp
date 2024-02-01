# Generated by Django 5.0 on 2024-02-01 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0050_remove_sortiepack_entreprise_remove_sortiepack_pack_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandepf',
            name='table_number',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='commandefourniture',
            name='ref',
            field=models.CharField(default='6516b72d90', max_length=10),
        ),
        migrations.AlterField(
            model_name='commandemp',
            name='ref',
            field=models.CharField(default='cde5af10e6', max_length=10, verbose_name='réference'),
        ),
        migrations.AlterField(
            model_name='commandepf',
            name='ref',
            field=models.CharField(default='f584422b74', max_length=10, verbose_name='réference'),
        ),
    ]
