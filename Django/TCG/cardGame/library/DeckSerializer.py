from cardGame.models import Deck, Carte, CartePokemon

import logging
import random

logger = logging.getLogger(__name__)

class DeckSerializer():
    def __init__(self, deck:Deck):
        self.deck = deck
        self.cartes = []
        if self.deck is not None:
            for i in str(self.deck.liste).split(","):
                cartes = CartePokemon.objects.filter(id=int(i))
                if len(cartes) == 0: #pas une carte pokemon
                    self.cartes.append(Carte.objects.filter(id=int(i)).first())
                else:
                    self.cartes.append(cartes.first())

    def getCarte(self, i):
        return self.cartes[i]

    def pioche1Carte(self):
        cartePiochee = self.cartes[0]
        self.cartes = self.cartes[1:]
        #logger.error(cartePiochee)
        #logger.error([str(item) for item in self.cartes])
        return cartePiochee

    def pioche7Cartes(self):
        cartesPiochees = self.cartes[0:7]
        self.cartes = self.cartes[7:]
        #logger.error(cartesPiochees)
        #logger.error([str(item) for item in self.cartes])
        return cartesPiochees

    def melange(self):
        random.shuffle(self.cartes)

    def __str__(self):
        return str(self.cartes)

    def nbCartes(self):
        return len(self.cartes)
