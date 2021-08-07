from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from recettes.models import Ingredient, Recette


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

ingredients_selectionnes = []

def transfo_index():
    ingredients = Ingredient.objects.order_by('nom')
    ingredients_liste = []
    ingredients_choisis = []

    #change la liste d' ingredients en liste a deux dimension de longueur 10
    for i in range(0, ingredients.count(), 10):
        ingredients_liste.append(ingredients[i:(i+10)])

    #change la liste d' ingredients choisis en liste a deux dimension de longueur 10
    for i in range(0, len(ingredients_selectionnes), 10):
        ingredients_choisis.append(ingredients_selectionnes[i:(i+10)])

    return ingredients_liste, ingredients_choisis

def transfo_recettes(recettes):
    recettes_choisies = []
    ingredients_choisis = []

    #change la liste de recettes en liste a deux dimension de longueur 10
    for i in range(0, recettes.count(), 10):
        recettes_choisies.append(recettes[i:(i+10)])

    #change la liste d' ingredients choisis en liste a deux dimension de longueur 10
    for i in range(0, len(ingredients_selectionnes), 10):
        ingredients_choisis.append(ingredients_selectionnes[i:(i+10)])

    return recettes_choisies, ingredients_choisis

    

def index(request):
    ingredients_selectionnes.clear()

    ingredients_liste, ingredients_choisis = transfo_index()

    context = {
        'ingredients_liste'    : ingredients_liste,
        'ingredients_choisis' : ingredients_choisis,
    }
    return render(request, 'recettes/index.html', context)

def ajouter_ingredient(request, id):
    ingredient = Ingredient.objects.get(pk = id)

    if ingredient not in ingredients_selectionnes:
        ingredients_selectionnes.append(ingredient)

    ingredients_liste, ingredients_choisis = transfo_index()

    context = {
        'ingredients_liste'    : ingredients_liste,
        'ingredients_choisis'  : ingredients_choisis
    }
    return render(request, 'recettes/index.html', context)

def supprimer_ingredient(request, id):

    ingredient = Ingredient.objects.get(pk = id)

    if ingredient in ingredients_selectionnes:
        ingredients_selectionnes.remove(ingredient)

    ingredients_liste, ingredients_choisis = transfo_index()

    context = {
        'ingredients_liste'    : ingredients_liste,
        'ingredients_choisis'  : ingredients_choisis
    }
    return render(request, 'recettes/index.html', context)

def filtrer(request):

    recettes_liste = Recette.objects.all()

    for ingredient in ingredients_selectionnes:
        recettes_liste = recettes_liste.filter(ingredients = ingredient)

    recettes_choisies, ingredients_choisis = transfo_recettes(recettes_liste)

    context = {
        'recettes_choisies'         : recettes_choisies,
        'ingredients_choisis'       : ingredients_choisis
    }
    return render(request, 'recettes/filtrer.html', context)

def detail(request, id):

    recette = Recette.objects.get(pk = id)

    context = {
        'recette'    : recette,
    }
    return render(request, 'recettes/detail.html', context)