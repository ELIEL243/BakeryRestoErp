# Generated by Django 5.0 on 2024-06-03 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0055_alter_commandefourniture_ref_alter_commandemp_ref_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sortiemp',
            name='destination',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='sortiepf',
            name='destination',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='commandefourniture',
            name='ref',
            field=models.CharField(default='850c9d1da1', max_length=10),
        ),
        migrations.AlterField(
            model_name='commandemp',
            name='ref',
            field=models.CharField(default='ed8539a178', max_length=10, verbose_name='réference'),
        ),
        migrations.AlterField(
            model_name='commandepf',
            name='ref',
            field=models.CharField(default='6e6cadab89', max_length=10, verbose_name='réference'),
        ),
    ]
