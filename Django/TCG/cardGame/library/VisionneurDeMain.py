from cardGame.models import Carte, CartePokemon
import logging

logger = logging.getLogger(__name__)

class VisionneurDeMain():
    def __init__(self):
        self.main = []
        self.index = 0

    def ajouterPlusieursCartes(self, liste):
        self.main = self.main + liste

    def ajouterCarte(self, carte:Carte):
        #logger.error("ajouterCarte : "+str(carte)+" : isinstanceof : "+str(isinstance(carte, CartePokemon)))
        #if isinstance(carte, CartePokemon):
        #self.main = self.main + [CartePokemon(carte)]
        #else:
        self.main = self.main + [carte]
        logger.error("main : "+str(self.main))

    def retirercarte(self, i:int):
        carte = self.main[i+self.index]
        del self.main[i+self.index]
        if(len(self.main) == 8 and self.index > 0):#cas d'erreur : retirer une carteb ce qui change l'affichage et donc l'indexation
            self.index = self.index - 6
        return carte

    def getCard(self, i:int):
        return self.main[i]

    def getCartesVue9Plus(self):
        return self.main[self.index:self.index+6]

    def getCartesVue8Moins(self):
        return self.main

    def flecheArriere(self):
        if(self.index - 6 >= 0):
            self.index = self.index - 6

    def flecheAvant(self):
        if(self.index + 6 <= len(self.main)):
            self.index += 6
