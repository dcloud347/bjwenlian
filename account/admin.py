from django.contrib import admin
from .models import SchoolAccount, UserAccount,ClubAccount


# Register your models here.
@admin.register(SchoolAccount)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'check')
    list_filter = ['check']


@admin.register(UserAccount)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'basic', 'grade', 'signature','phone', 'check','school','avatar')
    list_filter = ['grade', 'phone', 'clubs', 'check']
    filter_horizontal = ('clubs',)


@admin.register(ClubAccount)
class ClubsAdmin(admin.ModelAdmin):
    list_display = ('name', 'simp_intro','full_intro','category', 'check','school','avatar')
    list_filter = ['name', 'category', 'check','school']