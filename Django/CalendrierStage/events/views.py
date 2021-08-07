# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse

from django.shortcuts import render

class IndexView(generic.ListView):
    template_name = 'events/index.html'
    context_object_name = 'latest_question_list'
    	
    def get_queryset(self):
        #Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        return HttpResponse("coucou");
    #def
#class
