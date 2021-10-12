from cardGame.models import CartePokemon

class Banc():
    def __init__(self):
        self.cartes = [None, None, None, None, None]

    def addCard(self, card:CartePokemon):
        for i in range(0,len(self.cartes)):
            if self.cartes[i] is None:
                return self.addCardIndex(card, i)
        return False

    def addCardIndex(self, card:CartePokemon, i:int):
        if(self.cartes[i] is not None or not isinstance(card, CartePokemon)):
            return False
        if(i >= 0 and i <= 4 and self.cartes[i] is None):
            self.cartes[i] = card
            return True

    def removeCard(self, card:CartePokemon, i:int):
        if(self.cartes[i] is None):
            return False
        if(i >= 0 and i <= 4 and cartes[i] is not None):
            self.cartes[i] = None
            return True

    def changeCard(self, card:CartePokemon, i:int):
        self.cartes[i] = card

    def getCard(self, i:int):
        return self.cartes[i]

    def getCardImage(self, i:int):
        if self.cartes[i] is None:
            return "contour.png"
        else:
            return self.cartes[i].image

    def getCard0(self):
        return self.getCardImage(0)

    def getCard1(self):
        return self.getCardImage(1)

    def getCard2(self):
        return self.getCardImage(2)

    def getCard3(self):
        return self.getCardImage(3)

    def getCard4(self):
        return self.getCardImage(4)
