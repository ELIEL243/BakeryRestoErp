# Generated by Django 5.0 on 2023-12-21 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakery', '0020_fourniture_critic_qts_matierepremiere_critic_qts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commandefourniture',
            name='ref',
            field=models.CharField(default='c0881d5922', max_length=10),
        ),
        migrations.AlterField(
            model_name='commandemp',
            name='ref',
            field=models.CharField(default='098fbc4557', max_length=10),
        ),
        migrations.AlterField(
            model_name='fourniture',
            name='critic_qts',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='matierepremiere',
            name='critic_qts',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='produitfini',
            name='critic_qts',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
