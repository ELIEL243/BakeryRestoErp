# Generated by Django 5.0 on 2023-12-21 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0017_alter_commandefourniture_ref_alter_commandemp_ref_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='entreefourniture',
            name='devise',
            field=models.CharField(choices=[('USD', 'USD'), ('FC', 'FC')], default=('FC', 'FC'), max_length=25),
        ),
        migrations.AddField(
            model_name='entreefourniture',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='commandefourniture',
            name='ref',
            field=models.CharField(default='8e9b24696e', max_length=10),
        ),
        migrations.AlterField(
            model_name='commandemp',
            name='ref',
            field=models.CharField(default='22ecfd8841', max_length=10),
        ),
    ]
