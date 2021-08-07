# Generated by Django 2.0.2 on 2018-06-10 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=20)),
                ('image', models.ImageField(default=None, upload_to='gallery')),
            ],
        ),
        migrations.CreateModel(
            name='Recette',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=20)),
                ('image', models.ImageField(default=None, upload_to='gallery')),
                ('preparation', models.CharField(max_length=20)),
                ('note', models.IntegerField()),
                ('ingredients', models.ManyToManyField(to='recettes.Ingredient')),
            ],
        ),
    ]
