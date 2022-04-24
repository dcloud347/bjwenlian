from django.contrib import admin
from .models import Attachment, Activities


# Register your models here.
class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0


@admin.register(Activities)
class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'time_create','club','check','like')
    list_filter = ['title', 'club']
    inlines = [AttachmentInline]