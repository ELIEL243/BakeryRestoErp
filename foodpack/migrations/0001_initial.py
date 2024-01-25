# Generated by Django 5.0 on 2024-01-24 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entreprise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('adresse', models.TextField(blank=True, null=True)),
                ('mail', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=14, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FoodPack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='prix')),
                ('total_entry', models.IntegerField(blank=True, default=0, null=True)),
                ('total_out', models.IntegerField(blank=True, default=0, null=True)),
                ('total_sale', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
            ],
            options={
                'verbose_name': 'Pack',
            },
        ),
        migrations.CreateModel(
            name='EntreePack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qts', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('heure', models.TimeField(auto_now_add=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('added_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('pack', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='foodpack.foodpack', verbose_name='pack')),
            ],
            options={
                'verbose_name': 'Entrées des packs',
            },
        ),
        migrations.CreateModel(
            name='InvenduPack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qts', models.IntegerField(blank=True, default=0, null=True)),
                ('date', models.DateField(null=True)),
                ('heure', models.TimeField(null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='cout total')),
                ('devise', models.CharField(choices=[('USD', 'USD'), ('FC', 'FC')], default='FC', max_length=25)),
                ('pack', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='foodpack.foodpack')),
            ],
            options={
                'verbose_name': 'Invendus de packs',
            },
        ),
        migrations.CreateModel(
            name='SortiePack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qts', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True, null=True)),
                ('heure', models.TimeField(auto_now_add=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='prix')),
                ('devise', models.CharField(choices=[('USD', 'USD'), ('FC', 'FC')], default='FC', max_length=25)),
                ('completed', models.BooleanField(default=False)),
                ('added_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('entreprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodpack.entreprise')),
                ('pack', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='foodpack.foodpack')),
            ],
            options={
                'verbose_name': 'Livraisons des packs',
            },
        ),
    ]
