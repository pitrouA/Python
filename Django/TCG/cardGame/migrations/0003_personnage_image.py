# Generated by Django 2.2.20 on 2021-10-08 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardGame', '0002_attaque_degats'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnage',
            name='image',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
