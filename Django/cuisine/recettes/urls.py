from django.urls import path
from cuisine import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ajouter_ingredient/<int:id>/', views.ajouter_ingredient, name='ajouter-ingredient'),
    path('supprimer_ingredient/<int:id>/', views.supprimer_ingredient, name='supprimer-ingredient'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('filtrer/', views.filtrer, name='filtrer'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
