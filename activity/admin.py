from django.contrib import admin
from .models import Activities,Passage
# Register your models here.


@admin.register(Activities)
class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'time_create','club','school','check','like')
    list_filter = ['title', 'school', 'club', 'check']

@admin.register(Passage)
class PassagesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author','check','school','like')
    list_filter = ['title', 'school', 'check','author']