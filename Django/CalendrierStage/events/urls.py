from django.urls import path
from django.views.generic.base import RedirectView
from django.urls import reverse
from . import views

app_name = 'events'

urlpatterns = [
	path('', views.IndexView.as_view(), name='index'),
]
