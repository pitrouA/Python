from django.contrib import admin

from recettes.models import Ingredient, Recette

admin.site.register(Ingredient)
admin.site.register(Recette)
