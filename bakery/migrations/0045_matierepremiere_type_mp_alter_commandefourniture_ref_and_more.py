# Generated by Django 5.0 on 2024-01-20 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0044_alter_commandefourniture_ref_alter_commandemp_ref_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='matierepremiere',
            name='type_mp',
            field=models.CharField(blank=True, choices=[('BOULANGERIE', 'BOULANGERIE'), ('RESTAURANT', 'RESTAURANT'), ('BOULANGERIE ET RESTAURANT', 'BOULANGERIE ET RESTAURANT')], max_length=100, null=True, verbose_name='type de matière'),
        ),
        migrations.AlterField(
            model_name='commandefourniture',
            name='ref',
            field=models.CharField(default='923d26608d', max_length=10),
        ),
        migrations.AlterField(
            model_name='commandemp',
            name='ref',
            field=models.CharField(default='906c7e9fdb', max_length=10, verbose_name='réference'),
        ),
        migrations.AlterField(
            model_name='commandepf',
            name='ref',
            field=models.CharField(default='82c12fd1af', max_length=10, verbose_name='réference'),
        ),
    ]
