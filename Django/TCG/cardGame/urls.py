from django.urls import path

from . import views

urlpatterns = [
    #path('selectBancPlayer/<int:cardPos>/', views.selectBancPlayer, name='selectBancPlayer'),
    #path('selectBancOpponent/<int:cardPos>/', views.selectBancOpponent, name='selectBancOpponent'),
    path('game', views.index, name='index'),
    path('test', views.test, name='test'),
    path('retraite', views.retraite, name='retraite'),
    path('attaque/<int:idAttaque>', views.attaque, name='attaque'),
    path('flecheAvant', views.flecheAvant, name='flecheAvant'),
    path('flecheArriere', views.flecheArriere, name='flecheArriere'),
    path('echangeRetraite/<str:typeZone>/<int:posZone>', views.echangeRetraite, name='echangeRetraite'),
    path('joueCarte/<str:typeZone>/<int:posZone>', views.joueCarte, name='joueCarte'),
    path('pokePower/<str:typeZone>/<int:posZone>', views.pokePower, name='pokePower'),
    path('changeSelection/<int:pos>/<str:type>', views.changeSelection, name='changeSelection'),

    #refresh methods
    path('refreshHand/<int:isPlayer>', views.refreshHand, name='refreshHand'),
    path('refreshBench/<int:pos>/<int:isPlayer>', views.refreshBench, name='refreshBench'),
    path('refreshActive/<int:pos>/<int:isPlayer>', views.refreshActive, name='refreshActive'),
    path('refreshModalPlayer/<str:typeZone>/<int:posZone>', views.refreshModalPlayer, name='refreshModalPlayer'),
    path('refreshPv/<str:typeZone>/<int:posZone>/<int:isPlayer>', views.refreshPv, name='refreshPv'),


    path('', views.newGame, name='newGame'),
]
