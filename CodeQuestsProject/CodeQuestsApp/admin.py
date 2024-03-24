from django.contrib import admin
from .models import *
from django.forms import modelformset_factory
from django import forms
from django.forms.models import inlineformset_factory

# Register your models here.

admin.site.register(MyUser)
admin.site.register(Task)
admin.site.register(Solution)
admin.site.register(Match)
admin.site.register(Achievement)
admin.site.register(Ranking)
admin.site.register(Table)
admin.site.register(Course)

# paz ovo znaci vjv ovdje treba dodat da se moze dodat zadtak u kurs odma iz kurs screena i to ces ti abd
