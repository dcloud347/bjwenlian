from django.contrib import admin

# Register your models here.
from Passage.models import Passage


@admin.register(Passage)
class PassagesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author','check','like')
    list_filter = ['title', 'check','author']