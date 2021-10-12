from django.db import models
# Create your models here.

class Effet(models.Model):
    power = models.IntegerField(default=0)

    def __str__ (self):
        return str(self.id)

class Attaque(models.Model):
    name = models.CharField(max_length=30)
    cout = models.TextField(blank=True)
    effet = models.ForeignKey(Effet,models.SET_NULL,blank=True,null=True,related_name='effetAttaque')
    degats = models.IntegerField(default=0)

    def __str__ (self):
        return str(self.id)+":"+self.name

class Power(models.Model):
    name = models.CharField(max_length=30)
    effet = models.ForeignKey(Effet,models.SET_NULL,blank=True,null=True,related_name='effetPouvoir')
    body = models.BooleanField(default=False)

    def __str__ (self):
        return str(self.id)+":"+self.name

class Type(models.Model):
    name = models.CharField(max_length=30)

    def __str__ (self):
        return str(self.id)+":"+self.name

class Personnage(models.Model):
    name = models.CharField(max_length=30)
    image = models.CharField(max_length=100, blank=True)

    def __str__ (self):
        return str(self.id)+":"+self.name

class Carte(models.Model):
    name = models.CharField(max_length=30)
    image = models.CharField(max_length=100, blank=True)
    rarity = models.IntegerField(default=0)

    def __str__ (self):
        return str(self.id)+":"+self.name

class CartePokemon(Carte):
    pv = models.IntegerField(default=0)
    type1 = models.ForeignKey(Type,models.SET_NULL,blank=True,null=True,related_name='type1')
    type2 = models.ForeignKey(Type,models.SET_NULL,blank=True,null=True,related_name='type2')
    level = models.IntegerField(default=0)

    pokePower = models.ForeignKey(Power,models.SET_NULL,blank=True,null=True,related_name='pokePower')
    pokeBody = models.ForeignKey(Power,models.SET_NULL,blank=True,null=True,related_name='pokeBody')

    attaques = models.ManyToManyField(Attaque)

    weakness = models.ForeignKey(Type,models.SET_NULL,blank=True,null=True,related_name='weakness')
    resistance = models.ManyToManyField(Type)
    retreatCost = models.IntegerField(default=0)

    brillant = models.BooleanField(default=False)
    obscur = models.BooleanField(default=False)

    delta = models.BooleanField(default=False)
    ex = models.BooleanField(default=False)
    shiny = models.BooleanField(default=False)

class CarteEnergie(Carte):
    type1 = models.ForeignKey(Type,models.SET_NULL,blank=True,null=True,related_name='type')
    base = models.BooleanField(default=True)

class CarteDresseur(Carte):
    pass

class CarteDresseurInstantane(Carte):
    effet = models.ForeignKey(Effet,models.SET_NULL,blank=True,null=True,related_name='effetCarteInstantane')

class CarteOutilPokemon(CarteDresseur):
    pokemon = models.ForeignKey(CartePokemon,models.SET_NULL,blank=True,null=True,related_name='pokemon')
    effet = models.ForeignKey(Effet,models.SET_NULL,blank=True,null=True, related_name='effetCarteOutil')

class CarteMachineTechnique(CarteOutilPokemon):
    attaque = models.ForeignKey(Attaque,models.SET_NULL,blank=True,null=True,related_name='attaque')

class CarteStade(CarteDresseur):
    effet = models.ForeignKey(Effet,models.SET_NULL,blank=True,null=True,related_name='effetCarteStade')

class CarteSupporter(CarteDresseur):
    effet = models.ForeignKey(Effet,models.SET_NULL,blank=True,null=True,related_name='effetCarteSupporter')

class Deck(models.Model):
    cartes = models.ManyToManyField(Carte)
    personnage = models.ForeignKey(Personnage,models.SET_NULL,blank=True,null=True,related_name='personnage')

    liste = models.TextField(blank=True)

    def set_list(self, element):
        if self.liste:
            self.liste = self.liste + "," + element
        else:
            self.liste = element

    def get_list(self):
        if self.list:
            return self.liste.split(",")
        return None

    def __str__ (self):
        return str(self.id)+":"+self.personnage.name
