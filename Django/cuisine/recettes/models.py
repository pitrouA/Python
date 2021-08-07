from django.db import models

class Ingredient(models.Model):
    nom = models.CharField(max_length=60)
    image = models.ImageField(upload_to="gallery", default=None)

    def __str__(self):
        return "Ingredient : %s" % (self.nom)

class Recette(models.Model):
    nom = models.CharField(max_length=60)
    image = models.ImageField(upload_to="gallery", default=None)
    ingredients = models.ManyToManyField(Ingredient)
    preparation = models.CharField(max_length=2000)
    note = models.IntegerField()

    def __str__(self):
        return "Recette : %s" % (self.nom)
