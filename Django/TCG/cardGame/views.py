from django.shortcuts import render
from django.http import HttpResponse
from .models import Carte, Personnage, Deck
from .library.DeckSerializer import DeckSerializer
from .library.Contenu import Contenu
from .library.Select import Select
from .library.TerrainJoueur import TerrainJoueur
from django.shortcuts import redirect
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

joueur = None
adversaire = None
selection = None
monEnum = None

def newGame(request):
    global joueur, adversaire, selection
    joueur = TerrainJoueur("Ash")
    adversaire = TerrainJoueur("Misty")

    joueur.pioche7Cartes()
    adversaire.pioche7Cartes()

    # joueur.joueCarteBanc(2)
    # adversaire.joueCarteBanc(3)
    # adversaire.joueCarteBancIndex(2, 4)
    adversaire.joueCarteActif(2)

    selection = Select(2,"joueurCarte")

    return redirect(index)

def test(request):
    joueur.pioche1Carte()
    adversaire.pioche1Carte()

    #return HttpResponse('Hello World!')
    HttpResponse(Contenu.contentHand(joueur, True))
    return HttpResponse(status=204)

def changeSelection(request, pos:int, type:str):
    selection.pos = pos
    selection.type = type

    return HttpResponse(status=204)

def joueCarte(request, typeZone:str, posZone:int):
    if selection.type == "joueurCarte" and typeZone == "zoneCarteBanc":
        if joueur.joueCarteBancIndex(selection.pos, posZone): #si la carte a bienété jouee
            changeSelection(request, posZone, "joueurCarteBanc")
        else:
            return HttpResponse(status=204)
    elif selection.type == "joueurCarte" and typeZone == "zoneCarteActif":
        if joueur.joueCarteActif(selection.pos):
            changeSelection(request, posZone, "joueurCartePokemonActif")
        else:
            return HttpResponse(status=204)
    else:
        return HttpResponse(status=204)  #ne rien faire ( pas de changement de selection sur une zone vide sans raison )

    context = {
        "main" : Contenu.contentHand(joueur, True),
        "banc" : Contenu.contentBench(joueur, posZone, True ),
        "actif" : Contenu.contentActive(joueur, posZone, True ),
        "id" : selection.pos,
    }

    return JsonResponse(context)

def pokePower(request, typeZone:str, posZone:int):

    joueur.pioche1Carte()
    adversaire.pioche1Carte()

    return HttpResponse(Contenu.contentHand(joueur, True))

def retraite(request):
    selection.toogleMode()

    return HttpResponse(Contenu.retraite(selection))

def echangeRetraite(request, typeZone:str, posZone:int):

    if(selection.action):
        joueur.echangeRetraite(selection.pos)
    else:
        return HttpResponse(status=204)  #ne rien faire ( pas de changement d'icone retraite pour rien )

    context = {
        "id" : selection.pos,
        # "banc" : Contenu.contentBench(joueur, selection.pos, True),
        # "actif" : Contenu.contentActive(joueur, posZone, True)
    }

    return JsonResponse(context)

def flecheArriere(request):
    joueur.main.flecheArriere()
    return HttpResponse(Contenu.contentHand(joueur, True))

def flecheAvant(request):
    global joueur

    joueur.main.flecheAvant()
    return HttpResponse(Contenu.contentHand(joueur, True))

def attaque(request, idAttaque:int):
    degats = joueur.pokemonActif.attaques.all()[idAttaque].degats
    adversaire.pokemonActif.pv -= degats

    return HttpResponse(204)

#----------------------- refresh functions -------------------------------------

def refreshHand(request, isPlayer:bool):
    player = adversaire
    if isPlayer:
        logger.error("hand isPlayer : "+str(isPlayer))
        player = joueur

    return HttpResponse(Contenu.contentHand(player, isPlayer))

def refreshBench(request, pos:int, isPlayer:bool):
    player = adversaire
    if isPlayer:
        logger.error("bench isPlayer : "+str(isPlayer)+" pos :"+str(pos))
        player = joueur
    return HttpResponse(Contenu.contentBench(player, pos, isPlayer))

def refreshActive(request, pos:int, isPlayer:bool):
    player = adversaire
    if isPlayer:
        logger.error("active isPlayer : "+str(isPlayer)+" pos :"+str(pos))
        player = joueur
    return HttpResponse(Contenu.contentActive(player, pos, isPlayer))

def refreshModalPlayer( request, typeZone:str, posZone:int ):
    if(typeZone=="joueurCartePokemonActif"):
        return HttpResponse(Contenu.modalActions(typeZone, posZone, selection, joueur.pokemonActif))
    elif(typeZone=="joueurCarteBanc"):
        return HttpResponse(Contenu.modalActions(typeZone, posZone, selection, joueur.banc.getCard(posZone)))
    else:
        return HttpResponse(204)

def refreshPv(request,typeZone:str, posZone:int, isPlayer:bool):
    player = adversaire
    if isPlayer:
        logger.error("pv isPlayer : "+str(isPlayer)+" posZone :"+str(posZone))
        player = joueur
    if(typeZone=="joueurCartePokemonActif" or typeZone=="adversaireCartePokemonActif"):
        return HttpResponse(Contenu.contentPv(player.pokemonActif))
    else:
        return HttpResponse(Contenu.contentPv(player.banc.getCard(posZone)))

#----------------------- index function -------------------------------------

def index(request):
    global joueur, adversaire, selection
    #cardList = Carte.objects.all()
    #template = loader.get_template('cardGame/index.html')

    context = {
        'joueur': joueur,
        'adversaire': adversaire,
        'selection': selection,
    }
    return render(request, 'cardGame/battlefield.html', context)
    #return HttpResponse("Hello, world. You're at the polls index.")
