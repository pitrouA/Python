# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
import datetime

class Feeling(models.Model):
    feeling = models.TextField(u'Feeling', help_text=u'Feeling', blank=True, null=True)
    
    def __str__(self):
        return self.feeling
    
class Work(models.Model):
    work = models.TextField(u'Work', help_text=u'Work', blank=True, null=True)
    
    def __str__(self):
        return self.work

class Event(models.Model):
    day = models.DateField(u'Day of the event', help_text=u'Day of the event') #, default=datetime.date.today
    feeling = models.ForeignKey(Feeling, on_delete=models.SET_NULL, null=True)
    work = models.ForeignKey(Work, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)

    class Meta:
        verbose_name = u'Scheduling'
        verbose_name_plural = u'Scheduling'

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.feeling) +"<br>"+ str(self.work) +"<br>"+ str(self.notes))

