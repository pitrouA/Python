from .DeckSerializer import DeckSerializer
from .Banc import Banc
from .VisionneurDeMain import VisionneurDeMain
from cardGame.models import Carte, CartePokemon, Personnage, Deck
import logging

logger = logging.getLogger(__name__)

class TerrainJoueur():
    def __init__(self, name):
        self.name = name
        self.personnage = Personnage.objects.filter(name=self.name).first()
        self.main = VisionneurDeMain()
        self.pokemonActif = None
        self.banc = Banc()
        self.recompenses = ["verso.jpg","empty.png","verso.jpg","verso.jpg","verso.jpg","verso.jpg"]
        self.deck = DeckSerializer(Deck.objects.filter(personnage=self.personnage).first())
        self.defausse = ["machoc.png"]
        self.outilPokemon = None
        self.supporter = None
        self.stade = None

        self.melangeDeck()

    def getPlayer(self):
        return self.personnage

    def getDeck(self):
        return self.deck

    def pioche1Carte(self):
        self.main.ajouterCarte(self.deck.pioche1Carte())
        #logger.error(self.deck)

    def pioche7Cartes(self):
        self.main.ajouterPlusieursCartes(self.deck.pioche7Cartes())
        #logger.error(self.deck)

    def joueCarteBanc(self, i:int):
        carte = self.main.getCard(i)
        if(self.banc.addCard(carte)): #si l'ajout a été fait
            self.main.retirercarte(i)
            return True
        return False

    def joueCarteBancIndex(self, i:int, j:int):
        carte = self.main.getCard(i)
        if(self.banc.addCardIndex(carte, j)): #si l'ajout a été fait
            self.main.retirercarte(i)
            return True
        return False

    def joueCarteActif(self, i:int):
        carte = self.main.getCard(i)
        if self.pokemonActif != None or not isinstance(carte, CartePokemon):
            return False
        else:
            self.pokemonActif = self.main.retirercarte(i)
            return True


    def melangeDeck(self):
        self.deck.melange()

    def echangeRetraite(self, i:int):
        if self.pokemonActif != None and self.banc.getCard(i) != None :
            actif = self.pokemonActif
            self.pokemonActif = self.banc.getCard(i)
            self.banc.changeCard(actif, i)

    def getPokemonActifImage(self):
        if self.pokemonActif == None:
            return "contour.png"
        else:
            return self.pokemonActif.image
