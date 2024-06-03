# Generated by Django 5.0 on 2024-02-12 14:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0055_alter_commandefourniture_ref_alter_commandemp_ref_and_more'),
        ('foodpack', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntreeMpPack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qts', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('heure', models.TimeField(auto_now_add=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('added_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('matiere_premiere', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bakery.matierepremiere', verbose_name='matière première')),
            ],
            options={
                'verbose_name': 'Entrées de matière première.',
            },
        ),
        migrations.CreateModel(
            name='SortieMpPack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qts', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('heure', models.TimeField(auto_now_add=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('added_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('matiere_premiere', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bakery.matierepremiere')),
            ],
            options={
                'verbose_name': 'Sortie de matière première au service pack',
            },
        ),
    ]