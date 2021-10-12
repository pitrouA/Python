from django.contrib import admin

# Register your models here.

from .models import  Attaque, Carte, CarteEnergie, CarteDresseur, CarteDresseurInstantane, CarteMachineTechnique, CarteOutilPokemon, CartePokemon, CarteStade, CarteSupporter, Deck, Effet, Personnage, Power, Type

admin.site.register(Attaque)
admin.site.register(Carte)
admin.site.register(CarteDresseur)
admin.site.register(CarteDresseurInstantane)
admin.site.register(CarteMachineTechnique)
admin.site.register(CarteOutilPokemon)
admin.site.register(CarteEnergie)
admin.site.register(CartePokemon)
admin.site.register(CarteStade)
admin.site.register(CarteSupporter)
admin.site.register(Deck)
admin.site.register(Effet)
admin.site.register(Personnage)
admin.site.register(Power)
admin.site.register(Type)
