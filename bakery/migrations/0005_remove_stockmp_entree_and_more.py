# Generated by Django 5.0 on 2023-12-18 12:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0004_taux_entreefourniture_completed_entreemp_completed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockmp',
            name='entree',
        ),
        migrations.RemoveField(
            model_name='stockmp',
            name='matiere_premiere',
        ),
        migrations.RemoveField(
            model_name='stockmp',
            name='sortie',
        ),
        migrations.RemoveField(
            model_name='stockpf',
            name='entree',
        ),
        migrations.RemoveField(
            model_name='stockpf',
            name='produit_fini',
        ),
        migrations.RemoveField(
            model_name='stockpf',
            name='sortie',
        ),
        migrations.RemoveField(
            model_name='commandefourniture',
            name='fourniture',
        ),
        migrations.RemoveField(
            model_name='commandefourniture',
            name='qts',
        ),
        migrations.RemoveField(
            model_name='commandemp',
            name='matiere_premiere',
        ),
        migrations.RemoveField(
            model_name='commandemp',
            name='qts',
        ),
        migrations.CreateModel(
            name='LigneCommandeFourniture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qts', models.IntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('commande', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bakery.commandefourniture')),
                ('fourniture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bakery.fourniture')),
            ],
        ),
        migrations.CreateModel(
            name='LigneCommandeMp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qts', models.IntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('commande', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bakery.commandemp')),
                ('matiere_premiere', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bakery.matierepremiere')),
            ],
        ),
        migrations.DeleteModel(
            name='StockFourniture',
        ),
        migrations.DeleteModel(
            name='StockMP',
        ),
        migrations.DeleteModel(
            name='StockPF',
        ),
    ]
