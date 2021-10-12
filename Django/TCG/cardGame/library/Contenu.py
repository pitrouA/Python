from .TerrainJoueur import TerrainJoueur
from .Select import Select
from django.templatetags.static import static
from cardGame.models import CartePokemon

class Contenu:

    @staticmethod
    def contentHand(joueur:TerrainJoueur, isPlayer:bool = True):
        type = ""
        image = ""
        if(isPlayer):
            type = "joueurCarte"
        else:
            type = "adversaireCarte rotateimg180"

        content = "<div class='divHand'><img src="+static("images/"+joueur.personnage.image)+"></div>"
        if (len(joueur.main.getCartesVue8Moins()) <= 8):
            for i, carte in enumerate(joueur.main.getCartesVue8Moins()):
                if isPlayer:
                    image = carte.image
                else:
                    image = "verso.jpg"
                content = content + "<div class='divHand'><img class='"+type+"' id="+str(i)+" src='"+static("images/"+image)+"'></div>"
        else:
            content = content + "<div class='divHand rotateimg180 flecheArriere'><img src="+static("images/fleche.jpg")+"></div>"
            for i, carte in enumerate(joueur.main.getCartesVue9Plus()):
                if isPlayer:
                    image = carte.image
                else:
                    image = "verso.jpg"
                content = content + "<div class='divHand'><img class='"+type+"' id="+str(i)+" src="+static("images/"+image)+"></div>"
            content = content + "<div class='divHand flecheAvant'><img src="+static("images/fleche.jpg")+"></div>"
        return content

    @staticmethod
    def contentBench(joueur:TerrainJoueur, posZone:int = 0, isPlayer:bool = True):
        content = "<img id='"+str(posZone)+"' src="+static("images/"+joueur.banc.getCardImage(posZone))+" "
        if (joueur.banc.getCardImage(posZone) != None):
            if isPlayer:
                content = content + "class='joueurCarteBanc' "
            else:
                content = content + "class='adversaireCarteBanc rotateimg180' "
        else:
            if isPlayer:
                content = content + "class='zoneCarteBanc' "
            else:
                content = content + "class='zoneCarteBancAdversaire rotateimg180' "
        return content + ">"

    @staticmethod
    def contentActive(joueur:TerrainJoueur, posZone:int, isPlayer:bool = True ):
        content = "<img id='"+str(posZone)+"' src="+static("images/"+joueur.getPokemonActifImage())+" "
        if (joueur.pokemonActif != None):
            if isPlayer:
                content = content + "class='joueurCartePokemonActif' "
            else:
                content = content + "class='adversaireCartePokemonActif rotateimg180' "
        else:
            if isPlayer:
                content = content + "class='zoneCarteActif' "
            else:
                content = content + "class='zoneCarteActifAdversaire rotateimg180' "

        return content + ">"

    @staticmethod
    def modalActions(typeZone:str, posZone:int, selection:Select, carte:CartePokemon):
        content = ""
        if(typeZone == "joueurCarteBanc" or typeZone == "joueurCartePokemonActif"):
          content = "<div class='actionPanneau'>"+Contenu.retraite(selection)+"<img class='icon pokePower' src='"+static("images/icon2.png")+"'>\
                    </div>"
        if(typeZone == "joueurCartePokemonActif"):
          content = content + "<div class='attaquePanneau'>"
          for i, attaque in enumerate(carte.attaques.all()):
              content = content + "<div class='attaque' id='"+str(i)+"'>"+attaque.name+"</div>"
          content = content + "</div>"
        return content

    @staticmethod
    def retraite(selection:Select):
        if(selection.action):
            return "<img class='icon retraite' src='"+static("images/icon1.png")+"'>"
        else:
            return "<img class='icon retraite' src='"+static("images/icon2.png")+"'>"

    @staticmethod
    def contentPv(carte:CartePokemon):
        return "<div class='pvIcon'>"+str(carte.pv)+"</div>"
